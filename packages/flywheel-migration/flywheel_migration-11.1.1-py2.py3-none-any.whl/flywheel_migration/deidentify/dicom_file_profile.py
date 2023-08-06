"""File profile for de-identifying dicom files"""
import collections
import datetime
import gzip
import logging
import os
import re

import pydicom
import pydicom.datadict
import pydicom.tag
import six

from ..util import date_delta, is_dicom
from .file_profile import FileProfile

log = logging.getLogger(__name__)

DICOM_TAG_HEX_RE = re.compile(r'^(0x)?[0-9a-fA-F]{8}$')
DICOM_TAG_TUPLE_RE = re.compile(r'\(\s*([0-9a-fA-F]{4})\s*,\s*([0-9a-fA-F]{4})\s*\)')
# match data element in sequence
DICOM_NESTED_RE = re.compile(r'^([0-9A-Fa-f]{8}|[\w]+)\.([\d]+)\.([0-9A-Fa-f]{8}|[\w]+)$')


class DicomTagStr(str):
    """Subclass of string that has a _dicom_tag and _is_sequence attribute"""
    def __new__(cls, value, *_args, **_kwargs):
        return super(DicomTagStr, cls).__new__(cls, value)

    def __init__(self, _value, tag=None, seq=False):
        super(DicomTagStr, self).__init__()
        self._dicom_tag = tag
        self._is_sequence = seq


def parse_tag(name):
    """Parse the given string to determine if it's a property or tag or nested.

    Params:
        name (str|int): The field name or tag value or nested sequence

    Returns:
        DicomTagStr
    """
    if isinstance(name, int):
        tag = pydicom.tag.Tag(name)
        return DicomTagStr(str(tag), tag)

    name = name.strip()
    match = DICOM_TAG_HEX_RE.match(name)
    if match:
        tag = pydicom.tag.Tag(int(name, 16))
        return DicomTagStr(name, tag)

    match = DICOM_TAG_TUPLE_RE.match(name)
    if match:
        tag = pydicom.tag.Tag(int(match.group(1) + match.group(2), 16))
        return DicomTagStr(name, tag)

    match = DICOM_NESTED_RE.match(name)
    if match:
        tag = re.findall(r'([0-9A-Fa-f]{8}|[\w]+)+', name)
        tag = [t if i % 2 == 0 else int(t) for i, t in enumerate(tag)]  # odd element are idx of Sequence
        return DicomTagStr(name, tag, seq=True)

    return DicomTagStr(name)


class DicomFileProfile(FileProfile):
    """Dicom implementation of load/save and remove/replace fields"""

    name = 'dicom'
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = ['StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID']

    def __init__(self):
        super(DicomFileProfile, self).__init__(packfile_type='dicom')

        self.patient_age_from_birthdate = False
        self.patient_age_units = None

        self.remove_private_tags = False

        # set of all lower-cased DICOM keywords, for later validate()
        self.lc_kw_dict = {
            keyword.lower(): keyword
            for keyword in pydicom.datadict.keyword_dict
            if keyword  # non-blank
        }

    def add_field(self, field):
        # Handle tag conversion for later
        field.fieldname = parse_tag(field.fieldname)
        super(DicomFileProfile, self).add_field(field)

    def create_file_state(self):
        """Create state object for processing files"""
        return {
            'series_uid': None,
            'session_uid': None,
            'sop_uids': set()
        }

    def get_dest_path(self, state, record, path):
        """Return default named based on SOPInstanceUID or one based on profile if defined"""
        # Destination path is sop_uid.modality.dcm
        sop_uid = self.get_value(state, record, 'SOPInstanceUID')
        if not sop_uid:
            return path
        modality = self.get_value(state, record, 'Modality') or 'NA'
        dest_path = u'{}.{}.dcm'.format(sop_uid, modality.replace('/', '_'))
        return dest_path

    def to_config(self):
        result = super(DicomFileProfile, self).to_config()

        result['patient-age-from-birthdate'] = self.patient_age_from_birthdate
        if self.patient_age_units:
            result['patient-age-units'] = self.patient_age_units

        result['remove-private-tags'] = self.remove_private_tags

        return result

    def load_config(self, config):
        super(DicomFileProfile, self).load_config(config)

        self.patient_age_from_birthdate = config.get('patient-age-from-birthdate', False)
        self.patient_age_units = config.get('patient-age-units')
        self.remove_private_tags = config.get('remove-private-tags', False)

    def load_record(self, state, src_fs, path):  # pylint: disable=too-many-branches
        modified = False
        try:
            with src_fs.open(path, 'rb') as f:
                # Extract gzipped dicoms
                _, ext = os.path.splitext(path)
                if ext.lower() == '.gz':
                    f = gzip.GzipFile(fileobj=f)

                # Read and decode the dicom
                dcm = pydicom.dcmread(f, force=True)

                # Remove private tags before decoding
                if self.remove_private_tags:
                    dcm.remove_private_tags()
                    modified = True

                dcm.decode()
        except Exception:  # pylint: disable=broad-except
            if not is_dicom(src_fs, path):
                log.warning('IGNORING %s - it is not a DICOM file!', path)
                return None, False
            if self.deid_name != 'none':
                log.warning('IGNORING %s - cannot deid an invalid DICOM file!', path)
                return None, False

            log.warning('Packing invalid dicom %s because deid profile is "none"', path)
            return True, False

        # Validate the series/session
        series_uid = dcm.get('SeriesInstanceUID')
        session_uid = dcm.get('StudyInstanceUID')

        if state['series_uid'] is not None:
            # Validate SeriesInstanceUID
            if series_uid != state['series_uid']:
                log.warning('DICOM %s has a different SeriesInstanceUID (%s) from the rest of the series: %s', path, series_uid, state['series_uid'])
            # Validate StudyInstanceUID
            elif session_uid != state['session_uid']:
                log.warning('DICOM %s has a different StudyInstanceUID (%s) from the rest of the series: %s', path, session_uid, state['session_uid'])
        else:
            state['series_uid'] = series_uid
            state['session_uid'] = session_uid

        # Validate SOPInstanceUID
        sop_uid = dcm.get('SOPInstanceUID')
        if sop_uid:
            if sop_uid in state['sop_uids']:
                log.error('DICOM %s re-uses SOPInstanceUID %s, and will be excluded!', path, sop_uid)
                return None, False
            state['sop_uids'].add(sop_uid)

        # Set patient age from date of birth, if specified
        if self.patient_age_from_birthdate:
            dob = dcm.get('PatientBirthDate')
            study_date = dcm.get('StudyDate')

            if dob and study_date:
                try:
                    study_date = datetime.datetime.strptime(study_date, self.date_format)
                    dob = datetime.datetime.strptime(dob, self.date_format)

                    # Max value from dcm.py:84
                    age, units = date_delta(dob, study_date, desired_unit=self.patient_age_units, max_value=960)
                    dcm.PatientAge = '%03d%s' % (age, units)
                    modified = True
                except ValueError as err:
                    log.debug('Unable to update patient age in file %s: %s', path, err)

        return dcm, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, 'wb') as f:
            record.save_as(f)

    def read_field(self, state, record, fieldname):
        # Ensure that value is a string
        dcm_tag = getattr(fieldname, '_dicom_tag', None)
        if dcm_tag:
            if isinstance(dcm_tag, list):
                value = self._find_field_if_sequence(record, dcm_tag).value
            else:
                value = record.get(dcm_tag)
        else:
            value = getattr(record, fieldname, None)

        if value is not None and not isinstance(value, six.string_types):
            if isinstance(value, collections.Sequence):
                value = ','.join([str(x) for x in value])
            else:  # Unknown value, just convert to string
                value = str(value)
        return value

    def _find_field_if_sequence(self, record, tag):
        """Return data element corresponding to tag"""
        if not len(tag) == 1:
            return self._find_field_if_sequence(record[tag[0]], tag[1:])
        return record[tag[0]]

    def remove_field(self, state, record, fieldname):
        dcm_tag = getattr(fieldname, '_dicom_tag', None)
        if dcm_tag:
            if isinstance(dcm_tag, list):
                self._remove_field_if_sequence(record, dcm_tag)
            elif dcm_tag in record:
                del record[dcm_tag]
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def _remove_field_if_sequence(self, record, tag):
        """remove value on tag list, recursively"""
        if len(tag) == 1:
            if tag in record:
                del record[tag[0]]
        else:
            try:
                self._remove_field_if_sequence(record[tag[0]], tag[1:])
            except (KeyError, ValueError):
                pass

    def replace_field(self, state, record, fieldname, value):
        dcm_tag = getattr(fieldname, '_dicom_tag', None)
        if dcm_tag:
            if isinstance(dcm_tag, list):
                de = self._find_field_if_sequence(record, dcm_tag)
                de.value = value
            else:
                record[dcm_tag].value = value
        else:
            setattr(record, fieldname, value)

    def validate(self):
        """Validate the profile, returning any errors.

        Returns:
            list(str): A list of error messages, or an empty list
        """
        errors = []
        for field in self.fields:
            # do not validate if name is a tag or nested
            if DICOM_TAG_HEX_RE.match(field.fieldname) \
                    or DICOM_TAG_TUPLE_RE.match(field.fieldname) \
                    or DICOM_NESTED_RE.match(field.fieldname):
                continue
            lc_field = field.fieldname.lower()
            if lc_field not in self.lc_kw_dict:
                errors.append("Not in DICOM keyword list: " + field.fieldname)
            # case difference; correct to proper DICOM spelling
            elif field.fieldname != self.lc_kw_dict[lc_field]:
                field.fieldname = self.lc_kw_dict[lc_field]
        return errors

import logging
from core.signals import register_service_signal
from datetime import datetime
from medical_data.models import MedicalRecord
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


def reset_medical_record_before_update(medical_record):
    medical_record.symptoms = None
    medical_record.diagnosis = None
    medical_record.hospital = None
    medical_record.health_facility = None
    medical_record.treatment = None


class MedicalDataService:
    def __init__(self, user):
        self.user = user

    @register_service_signal('medical_data_service.create_or_update')
    def create_or_update(self, data):
        now = datetime.now()
        data['audit_user_id'] = self.user.id_for_audit
        data['validity_from'] = now
        medical_record_uuid = data.pop('uuid', None)

        # action = INS_ACT_CREATE
        # audit_old_obj = None
        if medical_record_uuid:
            medical_record = MedicalRecord.objects.select_related(
                "health_facility", "insuree").get(uuid=medical_record_uuid)
            # audit_old_obj_id = medical_record.save_history()
            # audit_old_obj = MedicalRecord.objects.filter(
            # id=audit_old_obj_id).first()
            # reset the non required fields
            # (each update is 'complete', necessary to be able to set 'null')
            reset_medical_record_before_update(medical_record)
            [setattr(medical_record, key, data[key]) for key in data]
            # action = INS_ACT_UPDATE
        else:
            medical_record = MedicalRecord.objects.create(**data)
            # save_audit_log("medical_record", "MedicalRecord", "family",\
            # FAMILY_ACT_INS_ADD, insuree, audit_old_obj,
            #                self.user.username)
        medical_record.save()
        # Saving audit logs for history of insuree
        # save_audit_log("insuree", "Insuree", "insuree",\
        # action, insuree, audit_old_obj, self.user.username)
        return medical_record

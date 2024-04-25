import logging
import graphene
from graphql_jwt.exceptions import PermissionDenied

from insuree.models import Insuree
from core.schema import OpenIMISMutation
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from graphene import Mutation


from location.models import HealthFacility

from .apps import MedicalDataConfig
from .gql_queries import UpdateMedicalRecordInputType, \
    CreateMedicalRecordInputType
from .models import MedicalRecord
from .services import MedicalDataService

logger = logging.getLogger(__name__)


def update_or_create_medical_record(data, user):
    data.pop('client_mutation_id', None)
    data.pop('client_mutation_label', None)
    return MedicalDataService(user).create_or_update(data)


class CreateMedicalRecordMutation(OpenIMISMutation):
    _mutation_module = "medical_data"
    _mutation_class = "CreateMedicalRecordMutation"

    class Input(CreateMedicalRecordInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if type(user) is AnonymousUser or not user.id:
                raise ValidationError(
                    _("mutation.authentication_required"))
            if not user.has_perms(
                    MedicalDataConfig\
                            .gql_mutation_create_medical_record_perms):
                raise PermissionDenied(_("unauthorized"))
            health_facility_uuid = data.pop('health_facility_uuid')
            insuree_uuid = data.pop('insuree_uuid')
            health_facility = HealthFacility.objects.filter(
                uuid=health_facility_uuid).first()
            if not health_facility:
                raise ValidationError("Health Facility not found")
            insuree = Insuree.objects.filter(uuid=insuree_uuid).first()
            if not insuree:
                raise ValidationError("Insuree not found")
            data['health_facility'] = health_facility
            data['insuree'] = insuree
            MedicalRecord.objects.create(**data)
            return [{
                'message': "Success",
                'detail': 'Success'}
            ]
        except Exception as exc:
            return [{
                'message': "An error occurred",
                'detail': str(exc)}
            ]


class UpdateMedicalRecordMutation(OpenIMISMutation):
    _mutation_module = "medical_data"
    _mutation_class = "UpdateMedicalRecordMutation"

    class Input(UpdateMedicalRecordInputType):
        pass

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            if type(user) is AnonymousUser or not user.id:
                raise ValidationError(
                    _("mutation.authentication_required"))
            if not user.has_perms(
                    MedicalDataConfig\
                            .gql_mutation_update_medical_record_perms):
                raise PermissionDenied(_("unauthorized"))
            data['audit_user_id'] = user.id_for_audit
            # client_mutation_id = data.get("client_mutation_id")
            update_or_create_medical_record(data, user)
            # FamilyMutation.object_mutated(
            # user, client_mutation_id=client_mutation_id, family=family)
            return None
        except Exception as exc:
            logger.exception("Failed to update the medical Record")
            return [{
                'message': _("Failed to update the medical Record"),
                'detail': str(exc)}
            ]


class DeleteMedicalRecordMutation(Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            user = info.context.user
            if type(user) is AnonymousUser or not user.id:
                raise ValidationError(
                    _("mutation.authentication_required"))
            if not user.has_perms(
                    MedicalDataConfig.gql_mutation_delete_medical_record_perms):
                raise PermissionDenied(_("unauthorized"))
            obj = MedicalRecord.objects.filter(id=id).first()
            if obj:
                obj.delete()
                return [{
                    'message': _("Deleted successfully"),
                    'detail': _("Deleted successfully")}
                ]
            else:
                return [{
                    'message': _("Medical Record not found"),
                    'detail': _("Medical Record not found")}
                ]
        except Exception as e:
            logger.exception("Failed to update the medical Record")
            return [{
                'message': _("Failed to Delete the medical Record"),
                'detail': str(e)}
            ]

import graphene
from django.contrib.auth.models import AnonymousUser
from graphql_jwt.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from jsonschema import ValidationError

from core.schema import OrderedDjangoFilterConnectionField
from .apps import MedicalDataConfig
from .gql_mutations import UpdateMedicalRecordMutation, \
    DeleteMedicalRecordMutation, CreateMedicalRecordMutation
from .gql_queries import MedicalRecordGQLType


class Mutation(graphene.ObjectType):
    create_medical_record = CreateMedicalRecordMutation.Field()
    update_medical_record = UpdateMedicalRecordMutation.Field()
    delete_medical_record = DeleteMedicalRecordMutation.Field()


class Query(graphene.ObjectType):
    medical_records = OrderedDjangoFilterConnectionField(
        MedicalRecordGQLType,
        orderBy=graphene.List(of_type=graphene.String)
    )

    def resolve_medical_records(self, info, **kwargs):
        user = info.context.user
        if type(user) is AnonymousUser or not user.id:
            raise ValidationError(
                _("mutation.authentication_required"))
        if not user.has_perms(MedicalDataConfig.gql_query_medical_record_perms):
            raise PermissionDenied(_("unauthorized"))
        return MedicalRecordGQLType._meta.model.objects.all()

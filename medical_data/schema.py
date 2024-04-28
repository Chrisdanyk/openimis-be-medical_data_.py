import logging

import graphene
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from graphql_jwt.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from jsonschema import ValidationError
from core.schema import OrderedDjangoFilterConnectionField
from insuree.gql_mutations import CreateFamilyMutation
from insuree.models import Family
from .apps import MedicalDataConfig
from .gql_mutations import UpdateMedicalRecordMutation, \
    DeleteMedicalRecordMutation, CreateMedicalRecordMutation
from .gql_queries import MedicalRecordGQLType
from core.schema import signal_mutation_module_validate

logger = logging.getLogger("openimis." + __file__)


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
        if not user.has_perms(
                MedicalDataConfig.gql_query_medical_record_perms):
            raise PermissionDenied(_("unauthorized"))
        return MedicalRecordGQLType._meta.model.objects.all()


def on_family_mutation(kwargs, k='uuid'):
    errors = []
    family_uuid = kwargs['data'].get('uuid', None)
    if not family_uuid:
        return errors
    if 'jsonExt' not in kwargs['data']:
        errors.append(
            {'message': 'No jsonExt provided for the family mutation'})
        logger.error(errors)
    impacted_family = Family.objects.get(Q(uuid=family_uuid))
    # FamilyMutation.objects.create(
    #     family=impacted_family, mutation_id=kwargs['mutation_log_id'])
    logger.info(f"####### Test of the family mutation on the impacted family:\
     {impacted_family} #######")
    return errors


def on_mutation(sender, **kwargs):
    return {
        CreateFamilyMutation._mutation_class: on_family_mutation,
    }.get(sender._mutation_class, lambda x: [])(kwargs)


def bind_signals():
    signal_mutation_module_validate["insuree"].connect(on_mutation)

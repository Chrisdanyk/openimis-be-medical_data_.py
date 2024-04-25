import graphene
import logging
from graphene_django import DjangoObjectType

from core.schema import OpenIMISMutation
from .models import MedicalRecord
from core import ExtendedConnection


logger = logging.getLogger(__name__)


class MedicalRecordGQLType(DjangoObjectType):

    class Meta:
        model = MedicalRecord
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "symptoms": ["contains"],
            "diagnosis": ["contains"],
        }
        connection_class = ExtendedConnection


class CreateMedicalRecordInputType(OpenIMISMutation.Input):
    symptoms = graphene.String()
    treatment = graphene.String()
    diagnosis = graphene.String()
    health_facility_uuid = graphene.UUID()
    insuree_uuid = graphene.UUID()


class UpdateMedicalRecordInputType(OpenIMISMutation.Input):
    symptoms = graphene.String()
    treatment = graphene.String()
    diagnosis = graphene.String()
    uuid = graphene.UUID(required=True)
    health_facility_uuid = graphene.UUID()
    insuree_uuid = graphene.UUID()

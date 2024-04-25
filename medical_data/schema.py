import graphene
from core.schema import OrderedDjangoFilterConnectionField
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

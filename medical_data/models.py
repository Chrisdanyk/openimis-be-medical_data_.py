import uuid
from django.db import models
from graphql.execution.base import ResolveInfo


class MedicalRecord(models.Model):
    insuree = models.ForeignKey(
        'insuree.Insuree', null=True, blank=True,
        on_delete=models.DO_NOTHING)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    uuid = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    health_facility = models.ForeignKey(
        'location.HealthFacility', null=True, blank=True,
        on_delete=models.DO_NOTHING,
        related_name="medical_records"
    )

    @classmethod
    def get_queryset(cls, queryset, user):
        if not queryset:
            cls.objects.all()
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if user.is_anonymous:
            queryset = queryset.filter(id=-1)
        if user.is_superuser:
            return queryset

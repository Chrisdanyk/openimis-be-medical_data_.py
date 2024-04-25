import uuid
from django.db import models


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

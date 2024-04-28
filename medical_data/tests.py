from django.test import TestCase
from location.models import HealthFacility

from insuree.models import Insuree
from medical_data.models import MedicalRecord


class MedicalDataModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.insuree = Insuree.objects.create(name="Test Insuree")
        cls.health_facility = HealthFacility.objects.create(
            name="Test Facility")

    def test_create_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            insuree=self.insuree,
            symptoms="Test symptoms",
            diagnosis="Test diagnosis",
            treatment="Test treatment",
            health_facility=self.health_facility
        )
        all_medical_records = MedicalRecord.objects.all()
        self.assertEqual(medical_record.symptoms, "Test symptoms")
        self.assertEqual(medical_record.diagnosis, "Test diagnosis")
        self.assertEqual(medical_record.treatment, "Test treatment")
        self.assertEqual(medical_record.insuree, self.insuree)
        self.assertEqual(medical_record.health_facility, self.health_facility)
        self.assertGreater(len(all_medical_records), 0)

    def test_update_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            insuree=self.insuree,
            symptoms="Test symptoms",
            diagnosis="Test diagnosis",
            treatment="Test treatment",
            health_facility=self.health_facility
        )
        MedicalRecord.objects.filter(pk=medical_record.pk).update(
            symptoms="Updated symptoms",
            diagnosis="Updated diagnosis",
            treatment="Updated treatment"
        )
        self.assertEqual(medical_record.symptoms, "Updated symptoms")
        self.assertEqual(medical_record.diagnosis, "Updated diagnosis")
        self.assertEqual(medical_record.treatment, "Updated treatment")

    def test_delete_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            insuree=self.insuree,
            symptoms="Test symptoms",
            diagnosis="Test diagnosis",
            treatment="Test treatment",
            health_facility=self.health_facility
        )
        medical_record.delete()
        all_medical_records = MedicalRecord.objects.all()
        self.assertEqual(len(all_medical_records), 0)

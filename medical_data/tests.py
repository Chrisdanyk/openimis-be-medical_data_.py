import warnings

from django.test import TestCase


class ExampleImisTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this code when implementing tests
        warnings.warn("The example code in test case is still present.")

    def test_example_module_loaded_correctly(self):
        self.assertTrue(True)

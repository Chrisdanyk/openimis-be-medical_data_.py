from django.apps import AppConfig

MODULE_NAME = 'medical_data'
DEFAULT_CFG = {
    "gql_query_medical_record_perms": ["111001"],
    "gql_mutation_create_medical_record_perms": ["100001"],
    "gql_mutation_update_medical_record_perms": ["100101"],
    "gql_mutation_delete_medical_record_perms": ["100201"],
}


class MedicalDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = MODULE_NAME
    gql_query_medical_record_perms = []
    gql_mutation_create_medical_record_perms = []
    gql_mutation_update_medical_record_perms = []
    gql_mutation_delete_medical_record_perms = []

    def _configure_perms(self, cfg):
        MedicalDataConfig\
            .gql_query_medical_record_perms = \
            cfg['gql_query_medical_record_perms']

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(
            MODULE_NAME, DEFAULT_CFG)
        self._configure_perms(cfg)

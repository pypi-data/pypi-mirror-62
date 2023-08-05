""" Example: Shows how to get info about the service using the Dashboard endpoint.  """

import urllib3

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

# Configure API key authorization: APIKeyHeader
configuration = feersum_nlu.Configuration()

# configuration.api_key['AUTH_TOKEN'] = feersum_nlu_auth_token
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!

configuration.host = feersumnlu_host
print(configuration.host)

api_instance = feersum_nlu.DashboardApi(feersum_nlu.ApiClient(configuration))

print()

# === DANGER!!! - Set of models to be vaporised even if not trashed ===
kill_set = set()
kill_set.add("faq_model_name__faq_matcher")

try:
    print("Vaporising trashed models...", flush=True)
    dashboard_detail = api_instance.dashboard_get_details()  # type: feersum_nlu.models.dashboard_detail.DashboardDetail

    # print(" type(api_response)", type(dashboard_detail))
    # print(" api_response", dashboard_detail)
    # print()

    for model in dashboard_detail.model_list:
        print(".", end='', flush=True)

        # DANGER ! if (model.name != "massmart") and (model.model_type == "sim_word_entity_extractor"):
        if model.trashed or (str(model.name+"__"+model.model_type) in kill_set):
            print(str(model.name+"__"+model.model_type))

            if model.model_type == 'language_recogniser':
                api_instance = feersum_nlu.LanguageRecognisersApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.language_recogniser_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'text_classifier':
                api_instance = feersum_nlu.TextClassifiersApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.text_classifier_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'intent_classifier':
                api_instance = feersum_nlu.IntentClassifiersApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.intent_classifier_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'faq_matcher':
                api_instance = feersum_nlu.FaqMatchersApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.faq_matcher_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'duckling_entity_extractor':
                api_instance = feersum_nlu.DucklingEntityExtractorsApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.duckling_entity_extractor_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'person_name_entity_extractor':
                api_instance = feersum_nlu.PersonNameEntityExtractorsApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.person_name_entity_extractor_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'regex_entity_extractor':
                api_instance = feersum_nlu.RegexEntityExtractorsApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.regex_entity_extractor_vaporise(model.name)
                print("    VAPORISED.")
            elif model.model_type == 'sim_word_entity_extractor':
                api_instance = feersum_nlu.SimWordEntityExtractorsApi(feersum_nlu.ApiClient(configuration))
                instance_detail = api_instance.sim_word_entity_extractor_vaporise(model.name)
                print("    VAPORISED.")
            else:
                instance_detail = None
                print("    NOT!!! VAPORISED.")

    print(' done.', flush=True)

except ApiException as e:
    print("Exception when calling DashboardApi->dashboard_get_details: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)

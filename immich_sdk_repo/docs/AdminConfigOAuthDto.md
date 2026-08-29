# AdminConfigOAuthDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_management_url** | **str** | Account management URL | [optional] [default to '']
**allow_insecure_requests** | **bool** | Allow insecure requests | 
**auto_launch** | **bool** | Auto launch | 
**auto_register** | **bool** | Auto register | 
**button_text** | **str** | Button text | 
**client_id** | **str** | Client ID | 
**client_secret** | **str** | Client secret | 
**default_storage_quota** | **int** | Default storage quota | 
**enabled** | **bool** | Enabled | 
**end_session_endpoint** | **str** | End session endpoint | 
**issuer_url** | **str** | Issuer URL | 
**mobile_override_enabled** | **bool** | Mobile override enabled | 
**mobile_redirect_uri** | **str** | Mobile redirect URI (set to empty string to disable) | 
**profile_signing_algorithm** | **str** | Profile signing algorithm | 
**prompt** | **str** | OAuth prompt parameter (e.g. select_account, login, consent) | 
**role_claim** | **str** | Role claim | 
**scope** | **str** | Scope | 
**signing_algorithm** | **str** | Signing algorithm | 
**storage_label_claim** | **str** | Storage label claim | 
**storage_quota_claim** | **str** | Storage quota claim | 
**timeout** | **int** | Timeout | 
**token_endpoint_auth_method** | [**OAuthTokenEndpointAuthMethod**](OAuthTokenEndpointAuthMethod.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_o_auth_dto import AdminConfigOAuthDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigOAuthDto from a JSON string
admin_config_o_auth_dto_instance = AdminConfigOAuthDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigOAuthDto.to_json())

# convert the object into a dict
admin_config_o_auth_dto_dict = admin_config_o_auth_dto_instance.to_dict()
# create an instance of AdminConfigOAuthDto from a dict
admin_config_o_auth_dto_from_dict = AdminConfigOAuthDto.from_dict(admin_config_o_auth_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



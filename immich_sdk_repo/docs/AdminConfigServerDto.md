# AdminConfigServerDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**external_domain** | **str** | External domain | 
**login_page_message** | **str** | Login page message | 
**public_users** | **bool** | Public users | 

## Example

```python
from immich_sdk.models.admin_config_server_dto import AdminConfigServerDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigServerDto from a JSON string
admin_config_server_dto_instance = AdminConfigServerDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigServerDto.to_json())

# convert the object into a dict
admin_config_server_dto_dict = admin_config_server_dto_instance.to_dict()
# create an instance of AdminConfigServerDto from a dict
admin_config_server_dto_from_dict = AdminConfigServerDto.from_dict(admin_config_server_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



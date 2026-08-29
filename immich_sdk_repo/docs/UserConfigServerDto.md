# UserConfigServerDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**external_domain** | **str** | External domain | 
**login_page_message** | **str** | Login page message | 
**public_users** | **bool** | Public users | 

## Example

```python
from immich_sdk.models.user_config_server_dto import UserConfigServerDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigServerDto from a JSON string
user_config_server_dto_instance = UserConfigServerDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigServerDto.to_json())

# convert the object into a dict
user_config_server_dto_dict = user_config_server_dto_instance.to_dict()
# create an instance of UserConfigServerDto from a dict
user_config_server_dto_from_dict = UserConfigServerDto.from_dict(user_config_server_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



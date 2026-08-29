# ServerConfigDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**external_domain** | **str** | External domain URL | 
**is_initialized** | **bool** | Whether the server has been initialized | 
**is_onboarded** | **bool** | Whether the admin has completed onboarding | 
**login_page_message** | **str** | Login page message | 
**maintenance_mode** | **bool** | Whether maintenance mode is active | 
**map_dark_style_url** | **str** | Map dark style URL | 
**map_light_style_url** | **str** | Map light style URL | 
**min_faces** | **int** | People min faces server default | 
**oauth_account_management_url** | **str** | OAuth account management URL | [optional] [default to '']
**oauth_button_text** | **str** | OAuth button text | 
**public_users** | **bool** | Whether public user registration is enabled | 
**trash_days** | **int** | Number of days before trashed assets are permanently deleted | 
**user_delete_delay** | **int** | Delay in days before deleted users are permanently removed | 

## Example

```python
from immich_sdk.models.server_config_dto import ServerConfigDto

# TODO update the JSON string below
json = "{}"
# create an instance of ServerConfigDto from a JSON string
server_config_dto_instance = ServerConfigDto.from_json(json)
# print the JSON string representation of the object
print(ServerConfigDto.to_json())

# convert the object into a dict
server_config_dto_dict = server_config_dto_instance.to_dict()
# create an instance of ServerConfigDto from a dict
server_config_dto_from_dict = ServerConfigDto.from_dict(server_config_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



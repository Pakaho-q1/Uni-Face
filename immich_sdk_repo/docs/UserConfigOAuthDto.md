# UserConfigOAuthDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_launch** | **bool** | Auto launch | 
**button_text** | **str** | Button text | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.user_config_o_auth_dto import UserConfigOAuthDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigOAuthDto from a JSON string
user_config_o_auth_dto_instance = UserConfigOAuthDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigOAuthDto.to_json())

# convert the object into a dict
user_config_o_auth_dto_dict = user_config_o_auth_dto_instance.to_dict()
# create an instance of UserConfigOAuthDto from a dict
user_config_o_auth_dto_from_dict = UserConfigOAuthDto.from_dict(user_config_o_auth_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



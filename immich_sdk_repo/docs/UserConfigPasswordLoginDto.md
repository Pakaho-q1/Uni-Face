# UserConfigPasswordLoginDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.user_config_password_login_dto import UserConfigPasswordLoginDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigPasswordLoginDto from a JSON string
user_config_password_login_dto_instance = UserConfigPasswordLoginDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigPasswordLoginDto.to_json())

# convert the object into a dict
user_config_password_login_dto_dict = user_config_password_login_dto_instance.to_dict()
# create an instance of UserConfigPasswordLoginDto from a dict
user_config_password_login_dto_from_dict = UserConfigPasswordLoginDto.from_dict(user_config_password_login_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



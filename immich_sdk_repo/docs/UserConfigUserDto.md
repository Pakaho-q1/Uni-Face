# UserConfigUserDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_delay** | **int** | Delete delay | 

## Example

```python
from immich_sdk.models.user_config_user_dto import UserConfigUserDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigUserDto from a JSON string
user_config_user_dto_instance = UserConfigUserDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigUserDto.to_json())

# convert the object into a dict
user_config_user_dto_dict = user_config_user_dto_instance.to_dict()
# create an instance of UserConfigUserDto from a dict
user_config_user_dto_from_dict = UserConfigUserDto.from_dict(user_config_user_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AdminConfigUserDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_delay** | **int** | Delete delay | 

## Example

```python
from immich_sdk.models.admin_config_user_dto import AdminConfigUserDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigUserDto from a JSON string
admin_config_user_dto_instance = AdminConfigUserDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigUserDto.to_json())

# convert the object into a dict
admin_config_user_dto_dict = admin_config_user_dto_instance.to_dict()
# create an instance of AdminConfigUserDto from a dict
admin_config_user_dto_from_dict = AdminConfigUserDto.from_dict(admin_config_user_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



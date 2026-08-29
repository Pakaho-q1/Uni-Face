# AdminConfigPasswordLoginDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_password_login_dto import AdminConfigPasswordLoginDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigPasswordLoginDto from a JSON string
admin_config_password_login_dto_instance = AdminConfigPasswordLoginDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigPasswordLoginDto.to_json())

# convert the object into a dict
admin_config_password_login_dto_dict = admin_config_password_login_dto_instance.to_dict()
# create an instance of AdminConfigPasswordLoginDto from a dict
admin_config_password_login_dto_from_dict = AdminConfigPasswordLoginDto.from_dict(admin_config_password_login_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



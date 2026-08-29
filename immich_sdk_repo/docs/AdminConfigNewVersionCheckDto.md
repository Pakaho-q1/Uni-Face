# AdminConfigNewVersionCheckDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel** | [**ReleaseChannel**](ReleaseChannel.md) |  | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_new_version_check_dto import AdminConfigNewVersionCheckDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigNewVersionCheckDto from a JSON string
admin_config_new_version_check_dto_instance = AdminConfigNewVersionCheckDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigNewVersionCheckDto.to_json())

# convert the object into a dict
admin_config_new_version_check_dto_dict = admin_config_new_version_check_dto_instance.to_dict()
# create an instance of AdminConfigNewVersionCheckDto from a dict
admin_config_new_version_check_dto_from_dict = AdminConfigNewVersionCheckDto.from_dict(admin_config_new_version_check_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AdminConfigJobSettingsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**concurrency** | **int** | Concurrency | 

## Example

```python
from immich_sdk.models.admin_config_job_settings_dto import AdminConfigJobSettingsDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigJobSettingsDto from a JSON string
admin_config_job_settings_dto_instance = AdminConfigJobSettingsDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigJobSettingsDto.to_json())

# convert the object into a dict
admin_config_job_settings_dto_dict = admin_config_job_settings_dto_instance.to_dict()
# create an instance of AdminConfigJobSettingsDto from a dict
admin_config_job_settings_dto_from_dict = AdminConfigJobSettingsDto.from_dict(admin_config_job_settings_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



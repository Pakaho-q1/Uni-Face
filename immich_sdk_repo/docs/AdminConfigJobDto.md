# AdminConfigJobDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**background_task** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**editor** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**face_detection** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**integrity_check** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**library** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**metadata_extraction** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**migration** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**notifications** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**ocr** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**search** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**sidecar** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**smart_search** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**thumbnail_generation** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**video_conversion** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 
**workflow** | [**AdminConfigJobSettingsDto**](AdminConfigJobSettingsDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_job_dto import AdminConfigJobDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigJobDto from a JSON string
admin_config_job_dto_instance = AdminConfigJobDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigJobDto.to_json())

# convert the object into a dict
admin_config_job_dto_dict = admin_config_job_dto_instance.to_dict()
# create an instance of AdminConfigJobDto from a dict
admin_config_job_dto_from_dict = AdminConfigJobDto.from_dict(admin_config_job_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



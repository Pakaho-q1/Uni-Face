# AdminConfigDto

Configuration properties that are visible to the admin

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**backup** | [**AdminConfigBackupsDto**](AdminConfigBackupsDto.md) |  | 
**ffmpeg** | [**AdminConfigFFmpegDto**](AdminConfigFFmpegDto.md) |  | 
**image** | [**AdminConfigImageDto**](AdminConfigImageDto.md) |  | 
**integrity_checks** | [**AdminConfigIntegrityChecksDto**](AdminConfigIntegrityChecksDto.md) |  | 
**job** | [**AdminConfigJobDto**](AdminConfigJobDto.md) |  | 
**library** | [**AdminConfigLibraryDto**](AdminConfigLibraryDto.md) |  | 
**logging** | [**AdminConfigLoggingDto**](AdminConfigLoggingDto.md) |  | 
**machine_learning** | [**AdminConfigMachineLearningDto**](AdminConfigMachineLearningDto.md) |  | 
**map** | [**AdminConfigMapDto**](AdminConfigMapDto.md) |  | 
**metadata** | [**AdminConfigMetadataDto**](AdminConfigMetadataDto.md) |  | 
**new_version_check** | [**AdminConfigNewVersionCheckDto**](AdminConfigNewVersionCheckDto.md) |  | 
**nightly_tasks** | [**AdminConfigNightlyTasksDto**](AdminConfigNightlyTasksDto.md) |  | 
**notifications** | [**AdminConfigNotificationsDto**](AdminConfigNotificationsDto.md) |  | 
**oauth** | [**AdminConfigOAuthDto**](AdminConfigOAuthDto.md) |  | 
**password_login** | [**AdminConfigPasswordLoginDto**](AdminConfigPasswordLoginDto.md) |  | 
**reverse_geocoding** | [**AdminConfigReverseGeocodingDto**](AdminConfigReverseGeocodingDto.md) |  | 
**server** | [**AdminConfigServerDto**](AdminConfigServerDto.md) |  | 
**storage_template** | [**AdminConfigStorageTemplateDto**](AdminConfigStorageTemplateDto.md) |  | 
**templates** | [**AdminConfigTemplatesDto**](AdminConfigTemplatesDto.md) |  | 
**theme** | [**AdminConfigThemeDto**](AdminConfigThemeDto.md) |  | 
**trash** | [**AdminConfigTrashDto**](AdminConfigTrashDto.md) |  | 
**user** | [**AdminConfigUserDto**](AdminConfigUserDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_dto import AdminConfigDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigDto from a JSON string
admin_config_dto_instance = AdminConfigDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigDto.to_json())

# convert the object into a dict
admin_config_dto_dict = admin_config_dto_instance.to_dict()
# create an instance of AdminConfigDto from a dict
admin_config_dto_from_dict = AdminConfigDto.from_dict(admin_config_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



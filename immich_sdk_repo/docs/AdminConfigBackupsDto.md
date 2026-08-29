# AdminConfigBackupsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**database** | [**AdminConfigDatabaseBackupDto**](AdminConfigDatabaseBackupDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_backups_dto import AdminConfigBackupsDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigBackupsDto from a JSON string
admin_config_backups_dto_instance = AdminConfigBackupsDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigBackupsDto.to_json())

# convert the object into a dict
admin_config_backups_dto_dict = admin_config_backups_dto_instance.to_dict()
# create an instance of AdminConfigBackupsDto from a dict
admin_config_backups_dto_from_dict = AdminConfigBackupsDto.from_dict(admin_config_backups_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AdminConfigDatabaseBackupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron_expression** | **str** | Cron expression | 
**enabled** | **bool** | Enabled | 
**keep_last_amount** | **int** | Keep last amount | 

## Example

```python
from immich_sdk.models.admin_config_database_backup_dto import AdminConfigDatabaseBackupDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigDatabaseBackupDto from a JSON string
admin_config_database_backup_dto_instance = AdminConfigDatabaseBackupDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigDatabaseBackupDto.to_json())

# convert the object into a dict
admin_config_database_backup_dto_dict = admin_config_database_backup_dto_instance.to_dict()
# create an instance of AdminConfigDatabaseBackupDto from a dict
admin_config_database_backup_dto_from_dict = AdminConfigDatabaseBackupDto.from_dict(admin_config_database_backup_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# DatabaseBackupDeleteDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**backups** | **List[str]** | Backup filenames to delete | 

## Example

```python
from immich_sdk.models.database_backup_delete_dto import DatabaseBackupDeleteDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseBackupDeleteDto from a JSON string
database_backup_delete_dto_instance = DatabaseBackupDeleteDto.from_json(json)
# print the JSON string representation of the object
print(DatabaseBackupDeleteDto.to_json())

# convert the object into a dict
database_backup_delete_dto_dict = database_backup_delete_dto_instance.to_dict()
# create an instance of DatabaseBackupDeleteDto from a dict
database_backup_delete_dto_from_dict = DatabaseBackupDeleteDto.from_dict(database_backup_delete_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



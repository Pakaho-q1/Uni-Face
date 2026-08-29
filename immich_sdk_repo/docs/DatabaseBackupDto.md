# DatabaseBackupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filename** | **str** | Backup filename | 
**filesize** | **int** | Backup file size | 
**timezone** | **str** | Backup timezone | 

## Example

```python
from immich_sdk.models.database_backup_dto import DatabaseBackupDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseBackupDto from a JSON string
database_backup_dto_instance = DatabaseBackupDto.from_json(json)
# print the JSON string representation of the object
print(DatabaseBackupDto.to_json())

# convert the object into a dict
database_backup_dto_dict = database_backup_dto_instance.to_dict()
# create an instance of DatabaseBackupDto from a dict
database_backup_dto_from_dict = DatabaseBackupDto.from_dict(database_backup_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



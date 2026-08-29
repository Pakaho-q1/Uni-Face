# DatabaseBackupListResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**backups** | [**List[DatabaseBackupDto]**](DatabaseBackupDto.md) | List of backups | 

## Example

```python
from immich_sdk.models.database_backup_list_response_dto import DatabaseBackupListResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatabaseBackupListResponseDto from a JSON string
database_backup_list_response_dto_instance = DatabaseBackupListResponseDto.from_json(json)
# print the JSON string representation of the object
print(DatabaseBackupListResponseDto.to_json())

# convert the object into a dict
database_backup_list_response_dto_dict = database_backup_list_response_dto_instance.to_dict()
# create an instance of DatabaseBackupListResponseDto from a dict
database_backup_list_response_dto_from_dict = DatabaseBackupListResponseDto.from_dict(database_backup_list_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# MaintenanceDetectInstallStorageFolderDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**files** | **int** | Number of files in the folder | 
**folder** | [**StorageFolder**](StorageFolder.md) |  | 
**readable** | **bool** | Whether the folder is readable | 
**writable** | **bool** | Whether the folder is writable | 

## Example

```python
from immich_sdk.models.maintenance_detect_install_storage_folder_dto import MaintenanceDetectInstallStorageFolderDto

# TODO update the JSON string below
json = "{}"
# create an instance of MaintenanceDetectInstallStorageFolderDto from a JSON string
maintenance_detect_install_storage_folder_dto_instance = MaintenanceDetectInstallStorageFolderDto.from_json(json)
# print the JSON string representation of the object
print(MaintenanceDetectInstallStorageFolderDto.to_json())

# convert the object into a dict
maintenance_detect_install_storage_folder_dto_dict = maintenance_detect_install_storage_folder_dto_instance.to_dict()
# create an instance of MaintenanceDetectInstallStorageFolderDto from a dict
maintenance_detect_install_storage_folder_dto_from_dict = MaintenanceDetectInstallStorageFolderDto.from_dict(maintenance_detect_install_storage_folder_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



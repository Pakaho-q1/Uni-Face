# MaintenanceDetectInstallResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**storage** | [**List[MaintenanceDetectInstallStorageFolderDto]**](MaintenanceDetectInstallStorageFolderDto.md) |  | 

## Example

```python
from immich_sdk.models.maintenance_detect_install_response_dto import MaintenanceDetectInstallResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of MaintenanceDetectInstallResponseDto from a JSON string
maintenance_detect_install_response_dto_instance = MaintenanceDetectInstallResponseDto.from_json(json)
# print the JSON string representation of the object
print(MaintenanceDetectInstallResponseDto.to_json())

# convert the object into a dict
maintenance_detect_install_response_dto_dict = maintenance_detect_install_response_dto_instance.to_dict()
# create an instance of MaintenanceDetectInstallResponseDto from a dict
maintenance_detect_install_response_dto_from_dict = MaintenanceDetectInstallResponseDto.from_dict(maintenance_detect_install_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



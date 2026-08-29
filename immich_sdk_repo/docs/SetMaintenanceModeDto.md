# SetMaintenanceModeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | [**MaintenanceAction**](MaintenanceAction.md) |  | 
**restore_backup_filename** | **str** | Restore backup filename | [optional] 

## Example

```python
from immich_sdk.models.set_maintenance_mode_dto import SetMaintenanceModeDto

# TODO update the JSON string below
json = "{}"
# create an instance of SetMaintenanceModeDto from a JSON string
set_maintenance_mode_dto_instance = SetMaintenanceModeDto.from_json(json)
# print the JSON string representation of the object
print(SetMaintenanceModeDto.to_json())

# convert the object into a dict
set_maintenance_mode_dto_dict = set_maintenance_mode_dto_instance.to_dict()
# create an instance of SetMaintenanceModeDto from a dict
set_maintenance_mode_dto_from_dict = SetMaintenanceModeDto.from_dict(set_maintenance_mode_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



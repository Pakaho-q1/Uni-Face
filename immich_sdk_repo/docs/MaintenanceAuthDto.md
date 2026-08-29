# MaintenanceAuthDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** | Maintenance username | 

## Example

```python
from immich_sdk.models.maintenance_auth_dto import MaintenanceAuthDto

# TODO update the JSON string below
json = "{}"
# create an instance of MaintenanceAuthDto from a JSON string
maintenance_auth_dto_instance = MaintenanceAuthDto.from_json(json)
# print the JSON string representation of the object
print(MaintenanceAuthDto.to_json())

# convert the object into a dict
maintenance_auth_dto_dict = maintenance_auth_dto_instance.to_dict()
# create an instance of MaintenanceAuthDto from a dict
maintenance_auth_dto_from_dict = MaintenanceAuthDto.from_dict(maintenance_auth_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



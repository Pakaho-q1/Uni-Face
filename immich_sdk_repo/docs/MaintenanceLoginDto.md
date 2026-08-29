# MaintenanceLoginDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | Maintenance token | [optional] 

## Example

```python
from immich_sdk.models.maintenance_login_dto import MaintenanceLoginDto

# TODO update the JSON string below
json = "{}"
# create an instance of MaintenanceLoginDto from a JSON string
maintenance_login_dto_instance = MaintenanceLoginDto.from_json(json)
# print the JSON string representation of the object
print(MaintenanceLoginDto.to_json())

# convert the object into a dict
maintenance_login_dto_dict = maintenance_login_dto_instance.to_dict()
# create an instance of MaintenanceLoginDto from a dict
maintenance_login_dto_from_dict = MaintenanceLoginDto.from_dict(maintenance_login_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# MaintenanceStatusResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | [**MaintenanceAction**](MaintenanceAction.md) |  | 
**active** | **bool** |  | 
**error** | **str** |  | [optional] 
**progress** | **int** |  | [optional] 
**task** | **str** |  | [optional] 

## Example

```python
from immich_sdk.models.maintenance_status_response_dto import MaintenanceStatusResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of MaintenanceStatusResponseDto from a JSON string
maintenance_status_response_dto_instance = MaintenanceStatusResponseDto.from_json(json)
# print the JSON string representation of the object
print(MaintenanceStatusResponseDto.to_json())

# convert the object into a dict
maintenance_status_response_dto_dict = maintenance_status_response_dto_instance.to_dict()
# create an instance of MaintenanceStatusResponseDto from a dict
maintenance_status_response_dto_from_dict = MaintenanceStatusResponseDto.from_dict(maintenance_status_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



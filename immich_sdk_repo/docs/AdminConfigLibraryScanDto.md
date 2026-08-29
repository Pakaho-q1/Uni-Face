# AdminConfigLibraryScanDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron_expression** | **str** | Cron expression | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_library_scan_dto import AdminConfigLibraryScanDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigLibraryScanDto from a JSON string
admin_config_library_scan_dto_instance = AdminConfigLibraryScanDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigLibraryScanDto.to_json())

# convert the object into a dict
admin_config_library_scan_dto_dict = admin_config_library_scan_dto_instance.to_dict()
# create an instance of AdminConfigLibraryScanDto from a dict
admin_config_library_scan_dto_from_dict = AdminConfigLibraryScanDto.from_dict(admin_config_library_scan_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



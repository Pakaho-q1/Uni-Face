# AdminConfigLibraryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scan** | [**AdminConfigLibraryScanDto**](AdminConfigLibraryScanDto.md) |  | 
**watch** | [**AdminConfigLibraryWatchDto**](AdminConfigLibraryWatchDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_library_dto import AdminConfigLibraryDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigLibraryDto from a JSON string
admin_config_library_dto_instance = AdminConfigLibraryDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigLibraryDto.to_json())

# convert the object into a dict
admin_config_library_dto_dict = admin_config_library_dto_instance.to_dict()
# create an instance of AdminConfigLibraryDto from a dict
admin_config_library_dto_from_dict = AdminConfigLibraryDto.from_dict(admin_config_library_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



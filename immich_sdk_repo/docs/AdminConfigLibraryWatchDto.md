# AdminConfigLibraryWatchDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_library_watch_dto import AdminConfigLibraryWatchDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigLibraryWatchDto from a JSON string
admin_config_library_watch_dto_instance = AdminConfigLibraryWatchDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigLibraryWatchDto.to_json())

# convert the object into a dict
admin_config_library_watch_dto_dict = admin_config_library_watch_dto_instance.to_dict()
# create an instance of AdminConfigLibraryWatchDto from a dict
admin_config_library_watch_dto_from_dict = AdminConfigLibraryWatchDto.from_dict(admin_config_library_watch_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



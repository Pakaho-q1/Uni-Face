# UpdateLibraryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exclusion_patterns** | **List[str]** | Exclusion patterns (max 128) | [optional] 
**import_paths** | **List[str]** | Import paths (max 128) | [optional] 
**name** | **str** | Library name | [optional] 

## Example

```python
from immich_sdk.models.update_library_dto import UpdateLibraryDto

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateLibraryDto from a JSON string
update_library_dto_instance = UpdateLibraryDto.from_json(json)
# print the JSON string representation of the object
print(UpdateLibraryDto.to_json())

# convert the object into a dict
update_library_dto_dict = update_library_dto_instance.to_dict()
# create an instance of UpdateLibraryDto from a dict
update_library_dto_from_dict = UpdateLibraryDto.from_dict(update_library_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



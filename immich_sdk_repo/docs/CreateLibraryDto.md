# CreateLibraryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exclusion_patterns** | **List[str]** | Exclusion patterns (max 128) | [optional] 
**import_paths** | **List[str]** | Import paths (max 128) | [optional] 
**name** | **str** | Library name | [optional] 
**owner_id** | **UUID** | Owner user ID | 

## Example

```python
from immich_sdk.models.create_library_dto import CreateLibraryDto

# TODO update the JSON string below
json = "{}"
# create an instance of CreateLibraryDto from a JSON string
create_library_dto_instance = CreateLibraryDto.from_json(json)
# print the JSON string representation of the object
print(CreateLibraryDto.to_json())

# convert the object into a dict
create_library_dto_dict = create_library_dto_instance.to_dict()
# create an instance of CreateLibraryDto from a dict
create_library_dto_from_dict = CreateLibraryDto.from_dict(create_library_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



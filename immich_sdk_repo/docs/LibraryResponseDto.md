# LibraryResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_count** | **int** | Number of assets | 
**created_at** | **datetime** | Creation date | 
**exclusion_patterns** | **List[str]** | Exclusion patterns | 
**id** | **UUID** | Library ID | 
**import_paths** | **List[str]** | Import paths | 
**name** | **str** | Library name | 
**owner_id** | **UUID** | Owner user ID | 
**refreshed_at** | **datetime** | Last refresh date | 
**updated_at** | **datetime** | Last update date | 

## Example

```python
from immich_sdk.models.library_response_dto import LibraryResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of LibraryResponseDto from a JSON string
library_response_dto_instance = LibraryResponseDto.from_json(json)
# print the JSON string representation of the object
print(LibraryResponseDto.to_json())

# convert the object into a dict
library_response_dto_dict = library_response_dto_instance.to_dict()
# create an instance of LibraryResponseDto from a dict
library_response_dto_from_dict = LibraryResponseDto.from_dict(library_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



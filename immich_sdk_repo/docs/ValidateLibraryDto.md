# ValidateLibraryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exclusion_patterns** | **List[str]** | Exclusion patterns (max 128) | [optional] 
**import_paths** | **List[str]** | Import paths to validate (max 128) | [optional] 

## Example

```python
from immich_sdk.models.validate_library_dto import ValidateLibraryDto

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateLibraryDto from a JSON string
validate_library_dto_instance = ValidateLibraryDto.from_json(json)
# print the JSON string representation of the object
print(ValidateLibraryDto.to_json())

# convert the object into a dict
validate_library_dto_dict = validate_library_dto_instance.to_dict()
# create an instance of ValidateLibraryDto from a dict
validate_library_dto_from_dict = ValidateLibraryDto.from_dict(validate_library_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



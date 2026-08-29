# StringPatternFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ends_with** | **str** |  | [optional] 
**eq** | **str** |  | [optional] 
**var_in** | **List[str]** |  | [optional] 
**like** | **str** |  | [optional] 
**ne** | **str** |  | [optional] 
**not_in** | **List[str]** |  | [optional] 
**not_like** | **str** |  | [optional] 
**starts_with** | **str** |  | [optional] 

## Example

```python
from immich_sdk.models.string_pattern_filter import StringPatternFilter

# TODO update the JSON string below
json = "{}"
# create an instance of StringPatternFilter from a JSON string
string_pattern_filter_instance = StringPatternFilter.from_json(json)
# print the JSON string representation of the object
print(StringPatternFilter.to_json())

# convert the object into a dict
string_pattern_filter_dict = string_pattern_filter_instance.to_dict()
# create an instance of StringPatternFilter from a dict
string_pattern_filter_from_dict = StringPatternFilter.from_dict(string_pattern_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



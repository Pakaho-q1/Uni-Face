# StringFilterNullable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | **str** |  | [optional] 
**var_in** | **List[str]** |  | [optional] 
**ne** | **str** |  | [optional] 
**not_in** | **List[str]** |  | [optional] 

## Example

```python
from immich_sdk.models.string_filter_nullable import StringFilterNullable

# TODO update the JSON string below
json = "{}"
# create an instance of StringFilterNullable from a JSON string
string_filter_nullable_instance = StringFilterNullable.from_json(json)
# print the JSON string representation of the object
print(StringFilterNullable.to_json())

# convert the object into a dict
string_filter_nullable_dict = string_filter_nullable_instance.to_dict()
# create an instance of StringFilterNullable from a dict
string_filter_nullable_from_dict = StringFilterNullable.from_dict(string_filter_nullable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



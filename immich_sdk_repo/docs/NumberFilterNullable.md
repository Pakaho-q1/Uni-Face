# NumberFilterNullable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | **float** |  | [optional] 
**gt** | **float** |  | [optional] 
**gte** | **float** |  | [optional] 
**var_in** | **List[float]** |  | [optional] 
**lt** | **float** |  | [optional] 
**lte** | **float** |  | [optional] 
**ne** | **float** |  | [optional] 
**not_in** | **List[float]** |  | [optional] 

## Example

```python
from immich_sdk.models.number_filter_nullable import NumberFilterNullable

# TODO update the JSON string below
json = "{}"
# create an instance of NumberFilterNullable from a JSON string
number_filter_nullable_instance = NumberFilterNullable.from_json(json)
# print the JSON string representation of the object
print(NumberFilterNullable.to_json())

# convert the object into a dict
number_filter_nullable_dict = number_filter_nullable_instance.to_dict()
# create an instance of NumberFilterNullable from a dict
number_filter_nullable_from_dict = NumberFilterNullable.from_dict(number_filter_nullable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



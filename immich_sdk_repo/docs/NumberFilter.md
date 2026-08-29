# NumberFilter


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
from immich_sdk.models.number_filter import NumberFilter

# TODO update the JSON string below
json = "{}"
# create an instance of NumberFilter from a JSON string
number_filter_instance = NumberFilter.from_json(json)
# print the JSON string representation of the object
print(NumberFilter.to_json())

# convert the object into a dict
number_filter_dict = number_filter_instance.to_dict()
# create an instance of NumberFilter from a dict
number_filter_from_dict = NumberFilter.from_dict(number_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



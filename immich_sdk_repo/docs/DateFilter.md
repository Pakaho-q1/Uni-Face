# DateFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | **datetime** |  | [optional] 
**gt** | **datetime** |  | [optional] 
**gte** | **datetime** |  | [optional] 
**lt** | **datetime** |  | [optional] 
**lte** | **datetime** |  | [optional] 
**ne** | **datetime** |  | [optional] 

## Example

```python
from immich_sdk.models.date_filter import DateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DateFilter from a JSON string
date_filter_instance = DateFilter.from_json(json)
# print the JSON string representation of the object
print(DateFilter.to_json())

# convert the object into a dict
date_filter_dict = date_filter_instance.to_dict()
# create an instance of DateFilter from a dict
date_filter_from_dict = DateFilter.from_dict(date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



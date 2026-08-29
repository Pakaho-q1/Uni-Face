# DateFilterNullable


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
from immich_sdk.models.date_filter_nullable import DateFilterNullable

# TODO update the JSON string below
json = "{}"
# create an instance of DateFilterNullable from a JSON string
date_filter_nullable_instance = DateFilterNullable.from_json(json)
# print the JSON string representation of the object
print(DateFilterNullable.to_json())

# convert the object into a dict
date_filter_nullable_dict = date_filter_nullable_instance.to_dict()
# create an instance of DateFilterNullable from a dict
date_filter_nullable_from_dict = DateFilterNullable.from_dict(date_filter_nullable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



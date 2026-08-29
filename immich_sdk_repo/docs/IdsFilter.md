# IdsFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**all** | **List[UUID]** |  | [optional] 
**any** | **List[UUID]** |  | [optional] 
**var_none** | **List[UUID]** |  | [optional] 

## Example

```python
from immich_sdk.models.ids_filter import IdsFilter

# TODO update the JSON string below
json = "{}"
# create an instance of IdsFilter from a JSON string
ids_filter_instance = IdsFilter.from_json(json)
# print the JSON string representation of the object
print(IdsFilter.to_json())

# convert the object into a dict
ids_filter_dict = ids_filter_instance.to_dict()
# create an instance of IdsFilter from a dict
ids_filter_from_dict = IdsFilter.from_dict(ids_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



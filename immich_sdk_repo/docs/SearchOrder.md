# SearchOrder


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**direction** | [**AssetOrder**](AssetOrder.md) |  | [optional] 
**var_field** | [**SearchOrderField**](SearchOrderField.md) |  | [optional] 

## Example

```python
from immich_sdk.models.search_order import SearchOrder

# TODO update the JSON string below
json = "{}"
# create an instance of SearchOrder from a JSON string
search_order_instance = SearchOrder.from_json(json)
# print the JSON string representation of the object
print(SearchOrder.to_json())

# convert the object into a dict
search_order_dict = search_order_instance.to_dict()
# create an instance of SearchOrder from a dict
search_order_from_dict = SearchOrder.from_dict(search_order_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



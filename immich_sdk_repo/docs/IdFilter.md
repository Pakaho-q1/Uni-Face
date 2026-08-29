# IdFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | **UUID** |  | [optional] 
**ne** | **UUID** |  | [optional] 

## Example

```python
from immich_sdk.models.id_filter import IdFilter

# TODO update the JSON string below
json = "{}"
# create an instance of IdFilter from a JSON string
id_filter_instance = IdFilter.from_json(json)
# print the JSON string representation of the object
print(IdFilter.to_json())

# convert the object into a dict
id_filter_dict = id_filter_instance.to_dict()
# create an instance of IdFilter from a dict
id_filter_from_dict = IdFilter.from_dict(id_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



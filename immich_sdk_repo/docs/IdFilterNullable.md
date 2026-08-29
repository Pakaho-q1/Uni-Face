# IdFilterNullable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | **UUID** |  | [optional] 
**ne** | **UUID** |  | [optional] 

## Example

```python
from immich_sdk.models.id_filter_nullable import IdFilterNullable

# TODO update the JSON string below
json = "{}"
# create an instance of IdFilterNullable from a JSON string
id_filter_nullable_instance = IdFilterNullable.from_json(json)
# print the JSON string representation of the object
print(IdFilterNullable.to_json())

# convert the object into a dict
id_filter_nullable_dict = id_filter_nullable_instance.to_dict()
# create an instance of IdFilterNullable from a dict
id_filter_nullable_from_dict = IdFilterNullable.from_dict(id_filter_nullable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



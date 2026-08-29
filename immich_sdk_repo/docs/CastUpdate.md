# CastUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**g_cast_enabled** | **bool** | Whether Google Cast is enabled | [optional] 

## Example

```python
from immich_sdk.models.cast_update import CastUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of CastUpdate from a JSON string
cast_update_instance = CastUpdate.from_json(json)
# print the JSON string representation of the object
print(CastUpdate.to_json())

# convert the object into a dict
cast_update_dict = cast_update_instance.to_dict()
# create an instance of CastUpdate from a dict
cast_update_from_dict = CastUpdate.from_dict(cast_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



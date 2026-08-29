# CastResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**g_cast_enabled** | **bool** | Whether Google Cast is enabled | 

## Example

```python
from immich_sdk.models.cast_response import CastResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CastResponse from a JSON string
cast_response_instance = CastResponse.from_json(json)
# print the JSON string representation of the object
print(CastResponse.to_json())

# convert the object into a dict
cast_response_dict = cast_response_instance.to_dict()
# create an instance of CastResponse from a dict
cast_response_from_dict = CastResponse.from_dict(cast_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



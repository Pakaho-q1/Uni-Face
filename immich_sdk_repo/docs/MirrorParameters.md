# MirrorParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**axis** | [**MirrorAxis**](MirrorAxis.md) |  | 

## Example

```python
from immich_sdk.models.mirror_parameters import MirrorParameters

# TODO update the JSON string below
json = "{}"
# create an instance of MirrorParameters from a JSON string
mirror_parameters_instance = MirrorParameters.from_json(json)
# print the JSON string representation of the object
print(MirrorParameters.to_json())

# convert the object into a dict
mirror_parameters_dict = mirror_parameters_instance.to_dict()
# create an instance of MirrorParameters from a dict
mirror_parameters_from_dict = MirrorParameters.from_dict(mirror_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



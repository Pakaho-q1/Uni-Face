# RotateParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**angle** | **float** | Rotation angle in degrees | 

## Example

```python
from immich_sdk.models.rotate_parameters import RotateParameters

# TODO update the JSON string below
json = "{}"
# create an instance of RotateParameters from a JSON string
rotate_parameters_instance = RotateParameters.from_json(json)
# print the JSON string representation of the object
print(RotateParameters.to_json())

# convert the object into a dict
rotate_parameters_dict = rotate_parameters_instance.to_dict()
# create an instance of RotateParameters from a dict
rotate_parameters_from_dict = RotateParameters.from_dict(rotate_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



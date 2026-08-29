# CropParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | **int** | Height of the crop | 
**width** | **int** | Width of the crop | 
**x** | **int** | Top-Left X coordinate of crop | 
**y** | **int** | Top-Left Y coordinate of crop | 

## Example

```python
from immich_sdk.models.crop_parameters import CropParameters

# TODO update the JSON string below
json = "{}"
# create an instance of CropParameters from a JSON string
crop_parameters_instance = CropParameters.from_json(json)
# print the JSON string representation of the object
print(CropParameters.to_json())

# convert the object into a dict
crop_parameters_dict = crop_parameters_instance.to_dict()
# create an instance of CropParameters from a dict
crop_parameters_from_dict = CropParameters.from_dict(crop_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



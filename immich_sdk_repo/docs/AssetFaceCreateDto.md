# AssetFaceCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**height** | **int** | Face bounding box height | 
**image_height** | **int** | Image height in pixels | 
**image_width** | **int** | Image width in pixels | 
**person_id** | **UUID** | Person ID | 
**width** | **int** | Face bounding box width | 
**x** | **int** | Face bounding box X coordinate | 
**y** | **int** | Face bounding box Y coordinate | 

## Example

```python
from immich_sdk.models.asset_face_create_dto import AssetFaceCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetFaceCreateDto from a JSON string
asset_face_create_dto_instance = AssetFaceCreateDto.from_json(json)
# print the JSON string representation of the object
print(AssetFaceCreateDto.to_json())

# convert the object into a dict
asset_face_create_dto_dict = asset_face_create_dto_instance.to_dict()
# create an instance of AssetFaceCreateDto from a dict
asset_face_create_dto_from_dict = AssetFaceCreateDto.from_dict(asset_face_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



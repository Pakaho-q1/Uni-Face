# AssetFaceResponseDto

Asset face with person

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bounding_box_x1** | **int** | Bounding box X1 coordinate | 
**bounding_box_x2** | **int** | Bounding box X2 coordinate | 
**bounding_box_y1** | **int** | Bounding box Y1 coordinate | 
**bounding_box_y2** | **int** | Bounding box Y2 coordinate | 
**id** | **UUID** | Face ID | 
**image_height** | **int** | Image height in pixels | 
**image_width** | **int** | Image width in pixels | 
**person** | [**PersonResponseDto**](PersonResponseDto.md) |  | 
**source_type** | [**SourceType**](SourceType.md) |  | [optional] 

## Example

```python
from immich_sdk.models.asset_face_response_dto import AssetFaceResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetFaceResponseDto from a JSON string
asset_face_response_dto_instance = AssetFaceResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetFaceResponseDto.to_json())

# convert the object into a dict
asset_face_response_dto_dict = asset_face_response_dto_instance.to_dict()
# create an instance of AssetFaceResponseDto from a dict
asset_face_response_dto_from_dict = AssetFaceResponseDto.from_dict(asset_face_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



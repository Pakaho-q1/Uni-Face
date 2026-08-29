# SyncAssetFaceV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**bounding_box_x1** | **int** | Bounding box X1 | 
**bounding_box_x2** | **int** | Bounding box X2 | 
**bounding_box_y1** | **int** | Bounding box Y1 | 
**bounding_box_y2** | **int** | Bounding box Y2 | 
**id** | **UUID** | Asset face ID | 
**image_height** | **int** | Image height | 
**image_width** | **int** | Image width | 
**person_id** | **str** | Person ID | 
**source_type** | **str** | Source type | 

## Example

```python
from immich_sdk.models.sync_asset_face_v1 import SyncAssetFaceV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetFaceV1 from a JSON string
sync_asset_face_v1_instance = SyncAssetFaceV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetFaceV1.to_json())

# convert the object into a dict
sync_asset_face_v1_dict = sync_asset_face_v1_instance.to_dict()
# create an instance of SyncAssetFaceV1 from a dict
sync_asset_face_v1_from_dict = SyncAssetFaceV1.from_dict(sync_asset_face_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# SyncAssetFaceV2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**bounding_box_x1** | **int** | Bounding box X1 | 
**bounding_box_x2** | **int** | Bounding box X2 | 
**bounding_box_y1** | **int** | Bounding box Y1 | 
**bounding_box_y2** | **int** | Bounding box Y2 | 
**deleted_at** | **datetime** | Face deleted at | 
**id** | **UUID** | Asset face ID | 
**image_height** | **int** | Image height | 
**image_width** | **int** | Image width | 
**is_visible** | **bool** | Is the face visible in the asset | 
**person_id** | **str** | Person ID | 
**source_type** | **str** | Source type | 

## Example

```python
from immich_sdk.models.sync_asset_face_v2 import SyncAssetFaceV2

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetFaceV2 from a JSON string
sync_asset_face_v2_instance = SyncAssetFaceV2.from_json(json)
# print the JSON string representation of the object
print(SyncAssetFaceV2.to_json())

# convert the object into a dict
sync_asset_face_v2_dict = sync_asset_face_v2_instance.to_dict()
# create an instance of SyncAssetFaceV2 from a dict
sync_asset_face_v2_from_dict = SyncAssetFaceV2.from_dict(sync_asset_face_v2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



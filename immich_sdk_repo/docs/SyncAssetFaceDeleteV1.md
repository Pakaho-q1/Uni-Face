# SyncAssetFaceDeleteV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_face_id** | **UUID** | Asset face ID | 

## Example

```python
from immich_sdk.models.sync_asset_face_delete_v1 import SyncAssetFaceDeleteV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetFaceDeleteV1 from a JSON string
sync_asset_face_delete_v1_instance = SyncAssetFaceDeleteV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetFaceDeleteV1.to_json())

# convert the object into a dict
sync_asset_face_delete_v1_dict = sync_asset_face_delete_v1_instance.to_dict()
# create an instance of SyncAssetFaceDeleteV1 from a dict
sync_asset_face_delete_v1_from_dict = SyncAssetFaceDeleteV1.from_dict(sync_asset_face_delete_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



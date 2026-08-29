# SyncAssetV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum** | **str** | Checksum | 
**created_at** | **datetime** | Uploaded to Immich at | 
**deleted_at** | **datetime** | Deleted at | 
**duration** | **str** | Duration | 
**file_created_at** | **datetime** | File created at | 
**file_modified_at** | **datetime** | File modified at | 
**height** | **int** | Asset height | 
**id** | **UUID** | Asset ID | 
**is_edited** | **bool** | Is edited | 
**is_favorite** | **bool** | Is favorite | 
**library_id** | **str** | Library ID | 
**live_photo_video_id** | **str** | Live photo video ID | 
**local_date_time** | **datetime** | Local date time | 
**original_file_name** | **str** | Original file name | 
**owner_id** | **UUID** | Owner ID | 
**stack_id** | **str** | Stack ID | 
**thumbhash** | **str** | Thumbhash | 
**type** | [**AssetTypeEnum**](AssetTypeEnum.md) |  | 
**visibility** | [**AssetVisibility**](AssetVisibility.md) |  | 
**width** | **int** | Asset width | 

## Example

```python
from immich_sdk.models.sync_asset_v1 import SyncAssetV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetV1 from a JSON string
sync_asset_v1_instance = SyncAssetV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetV1.to_json())

# convert the object into a dict
sync_asset_v1_dict = sync_asset_v1_instance.to_dict()
# create an instance of SyncAssetV1 from a dict
sync_asset_v1_from_dict = SyncAssetV1.from_dict(sync_asset_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



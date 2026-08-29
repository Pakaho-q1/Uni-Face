# SyncAlbumV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Created at | 
**description** | **str** | Album description | 
**id** | **UUID** | Album ID | 
**is_activity_enabled** | **bool** | Is activity enabled | 
**name** | **str** | Album name | 
**order** | [**AssetOrder**](AssetOrder.md) |  | 
**owner_id** | **UUID** | Owner ID | 
**thumbnail_asset_id** | **str** | Thumbnail asset ID | 
**updated_at** | **datetime** | Updated at | 

## Example

```python
from immich_sdk.models.sync_album_v1 import SyncAlbumV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAlbumV1 from a JSON string
sync_album_v1_instance = SyncAlbumV1.from_json(json)
# print the JSON string representation of the object
print(SyncAlbumV1.to_json())

# convert the object into a dict
sync_album_v1_dict = sync_album_v1_instance.to_dict()
# create an instance of SyncAlbumV1 from a dict
sync_album_v1_from_dict = SyncAlbumV1.from_dict(sync_album_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# SyncMemoryAssetV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**memory_id** | **UUID** | Memory ID | 

## Example

```python
from immich_sdk.models.sync_memory_asset_v1 import SyncMemoryAssetV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncMemoryAssetV1 from a JSON string
sync_memory_asset_v1_instance = SyncMemoryAssetV1.from_json(json)
# print the JSON string representation of the object
print(SyncMemoryAssetV1.to_json())

# convert the object into a dict
sync_memory_asset_v1_dict = sync_memory_asset_v1_instance.to_dict()
# create an instance of SyncMemoryAssetV1 from a dict
sync_memory_asset_v1_from_dict = SyncMemoryAssetV1.from_dict(sync_memory_asset_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



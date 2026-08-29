# SyncAssetMetadataV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**key** | **str** | Key | 
**value** | **Dict[str, object]** | Value | 

## Example

```python
from immich_sdk.models.sync_asset_metadata_v1 import SyncAssetMetadataV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetMetadataV1 from a JSON string
sync_asset_metadata_v1_instance = SyncAssetMetadataV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetMetadataV1.to_json())

# convert the object into a dict
sync_asset_metadata_v1_dict = sync_asset_metadata_v1_instance.to_dict()
# create an instance of SyncAssetMetadataV1 from a dict
sync_asset_metadata_v1_from_dict = SyncAssetMetadataV1.from_dict(sync_asset_metadata_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



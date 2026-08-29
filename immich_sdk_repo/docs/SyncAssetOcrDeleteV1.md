# SyncAssetOcrDeleteV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **str** | Original asset ID of the deleted OCR entry | 
**deleted_at** | **datetime** | Timestamp when the OCR entry was deleted | 
**id** | **str** | Audit row ID of the deleted OCR entry | 

## Example

```python
from immich_sdk.models.sync_asset_ocr_delete_v1 import SyncAssetOcrDeleteV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetOcrDeleteV1 from a JSON string
sync_asset_ocr_delete_v1_instance = SyncAssetOcrDeleteV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetOcrDeleteV1.to_json())

# convert the object into a dict
sync_asset_ocr_delete_v1_dict = sync_asset_ocr_delete_v1_instance.to_dict()
# create an instance of SyncAssetOcrDeleteV1 from a dict
sync_asset_ocr_delete_v1_from_dict = SyncAssetOcrDeleteV1.from_dict(sync_asset_ocr_delete_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



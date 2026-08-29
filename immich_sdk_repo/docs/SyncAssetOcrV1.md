# SyncAssetOcrV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**box_score** | **float** | Confidence score of the bounding box | 
**id** | **UUID** | OCR entry ID | 
**is_visible** | **bool** | Whether the OCR entry is visible | 
**text** | **str** | Recognized text content | 
**text_score** | **float** | Confidence score of the recognized text | 
**x1** | **float** | Top-left X coordinate (normalized 0–1) | 
**x2** | **float** | Top-right X coordinate (normalized 0–1) | 
**x3** | **float** | Bottom-right X coordinate (normalized 0–1) | 
**x4** | **float** | Bottom-left X coordinate (normalized 0–1) | 
**y1** | **float** | Top-left Y coordinate (normalized 0–1) | 
**y2** | **float** | Top-right Y coordinate (normalized 0–1) | 
**y3** | **float** | Bottom-right Y coordinate (normalized 0–1) | 
**y4** | **float** | Bottom-left Y coordinate (normalized 0–1) | 

## Example

```python
from immich_sdk.models.sync_asset_ocr_v1 import SyncAssetOcrV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetOcrV1 from a JSON string
sync_asset_ocr_v1_instance = SyncAssetOcrV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetOcrV1.to_json())

# convert the object into a dict
sync_asset_ocr_v1_dict = sync_asset_ocr_v1_instance.to_dict()
# create an instance of SyncAssetOcrV1 from a dict
sync_asset_ocr_v1_from_dict = SyncAssetOcrV1.from_dict(sync_asset_ocr_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



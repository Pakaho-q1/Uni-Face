# AssetOcrResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** |  | 
**box_score** | **float** | Confidence score for text detection box | 
**id** | **UUID** |  | 
**text** | **str** | Recognized text | 
**text_score** | **float** | Confidence score for text recognition | 
**x1** | **float** | Normalized x coordinate of box corner 1 (0-1) | 
**x2** | **float** | Normalized x coordinate of box corner 2 (0-1) | 
**x3** | **float** | Normalized x coordinate of box corner 3 (0-1) | 
**x4** | **float** | Normalized x coordinate of box corner 4 (0-1) | 
**y1** | **float** | Normalized y coordinate of box corner 1 (0-1) | 
**y2** | **float** | Normalized y coordinate of box corner 2 (0-1) | 
**y3** | **float** | Normalized y coordinate of box corner 3 (0-1) | 
**y4** | **float** | Normalized y coordinate of box corner 4 (0-1) | 

## Example

```python
from immich_sdk.models.asset_ocr_response_dto import AssetOcrResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetOcrResponseDto from a JSON string
asset_ocr_response_dto_instance = AssetOcrResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetOcrResponseDto.to_json())

# convert the object into a dict
asset_ocr_response_dto_dict = asset_ocr_response_dto_instance.to_dict()
# create an instance of AssetOcrResponseDto from a dict
asset_ocr_response_dto_from_dict = AssetOcrResponseDto.from_dict(asset_ocr_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



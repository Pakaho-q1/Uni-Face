# AssetFileResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Creation date | 
**id** | **UUID** | Asset file ID | 
**is_edited** | **bool** | The file was generated from an edit | 
**is_progressive** | **bool** | The file is a progressively encoded JPEG | 
**is_transparent** | **bool** | The file is transparent | 
**path** | **str** | File path | 
**type** | [**AssetFileType**](AssetFileType.md) |  | 
**updated_at** | **datetime** | Update date | 

## Example

```python
from immich_sdk.models.asset_file_response_dto import AssetFileResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetFileResponseDto from a JSON string
asset_file_response_dto_instance = AssetFileResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetFileResponseDto.to_json())

# convert the object into a dict
asset_file_response_dto_dict = asset_file_response_dto_instance.to_dict()
# create an instance of AssetFileResponseDto from a dict
asset_file_response_dto_from_dict = AssetFileResponseDto.from_dict(asset_file_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AssetMediaResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | Asset media ID | 
**status** | [**AssetMediaStatus**](AssetMediaStatus.md) |  | 

## Example

```python
from immich_sdk.models.asset_media_response_dto import AssetMediaResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetMediaResponseDto from a JSON string
asset_media_response_dto_instance = AssetMediaResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetMediaResponseDto.to_json())

# convert the object into a dict
asset_media_response_dto_dict = asset_media_response_dto_instance.to_dict()
# create an instance of AssetMediaResponseDto from a dict
asset_media_response_dto_from_dict = AssetMediaResponseDto.from_dict(asset_media_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



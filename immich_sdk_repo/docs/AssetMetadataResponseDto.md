# AssetMetadataResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Metadata key | 
**updated_at** | **datetime** | Last update date | 
**value** | **Dict[str, object]** | Metadata value (object) | 

## Example

```python
from immich_sdk.models.asset_metadata_response_dto import AssetMetadataResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetMetadataResponseDto from a JSON string
asset_metadata_response_dto_instance = AssetMetadataResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetMetadataResponseDto.to_json())

# convert the object into a dict
asset_metadata_response_dto_dict = asset_metadata_response_dto_instance.to_dict()
# create an instance of AssetMetadataResponseDto from a dict
asset_metadata_response_dto_from_dict = AssetMetadataResponseDto.from_dict(asset_metadata_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



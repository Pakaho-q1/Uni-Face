# AssetMetadataBulkResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**key** | **str** | Metadata key | 
**updated_at** | **datetime** | Last update date | 
**value** | **Dict[str, object]** | Metadata value (object) | 

## Example

```python
from immich_sdk.models.asset_metadata_bulk_response_dto import AssetMetadataBulkResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetMetadataBulkResponseDto from a JSON string
asset_metadata_bulk_response_dto_instance = AssetMetadataBulkResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetMetadataBulkResponseDto.to_json())

# convert the object into a dict
asset_metadata_bulk_response_dto_dict = asset_metadata_bulk_response_dto_instance.to_dict()
# create an instance of AssetMetadataBulkResponseDto from a dict
asset_metadata_bulk_response_dto_from_dict = AssetMetadataBulkResponseDto.from_dict(asset_metadata_bulk_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



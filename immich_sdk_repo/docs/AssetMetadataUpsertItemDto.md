# AssetMetadataUpsertItemDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | Metadata key | 
**value** | **Dict[str, object]** | Metadata value (object) | 

## Example

```python
from immich_sdk.models.asset_metadata_upsert_item_dto import AssetMetadataUpsertItemDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetMetadataUpsertItemDto from a JSON string
asset_metadata_upsert_item_dto_instance = AssetMetadataUpsertItemDto.from_json(json)
# print the JSON string representation of the object
print(AssetMetadataUpsertItemDto.to_json())

# convert the object into a dict
asset_metadata_upsert_item_dto_dict = asset_metadata_upsert_item_dto_instance.to_dict()
# create an instance of AssetMetadataUpsertItemDto from a dict
asset_metadata_upsert_item_dto_from_dict = AssetMetadataUpsertItemDto.from_dict(asset_metadata_upsert_item_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



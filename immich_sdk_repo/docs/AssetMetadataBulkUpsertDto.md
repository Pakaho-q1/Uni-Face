# AssetMetadataBulkUpsertDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[AssetMetadataBulkUpsertItemDto]**](AssetMetadataBulkUpsertItemDto.md) | Metadata items to upsert | 

## Example

```python
from immich_sdk.models.asset_metadata_bulk_upsert_dto import AssetMetadataBulkUpsertDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetMetadataBulkUpsertDto from a JSON string
asset_metadata_bulk_upsert_dto_instance = AssetMetadataBulkUpsertDto.from_json(json)
# print the JSON string representation of the object
print(AssetMetadataBulkUpsertDto.to_json())

# convert the object into a dict
asset_metadata_bulk_upsert_dto_dict = asset_metadata_bulk_upsert_dto_instance.to_dict()
# create an instance of AssetMetadataBulkUpsertDto from a dict
asset_metadata_bulk_upsert_dto_from_dict = AssetMetadataBulkUpsertDto.from_dict(asset_metadata_bulk_upsert_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



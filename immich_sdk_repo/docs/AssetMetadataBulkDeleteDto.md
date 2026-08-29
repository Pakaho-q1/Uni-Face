# AssetMetadataBulkDeleteDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[AssetMetadataBulkDeleteItemDto]**](AssetMetadataBulkDeleteItemDto.md) | Metadata items to delete | 

## Example

```python
from immich_sdk.models.asset_metadata_bulk_delete_dto import AssetMetadataBulkDeleteDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetMetadataBulkDeleteDto from a JSON string
asset_metadata_bulk_delete_dto_instance = AssetMetadataBulkDeleteDto.from_json(json)
# print the JSON string representation of the object
print(AssetMetadataBulkDeleteDto.to_json())

# convert the object into a dict
asset_metadata_bulk_delete_dto_dict = asset_metadata_bulk_delete_dto_instance.to_dict()
# create an instance of AssetMetadataBulkDeleteDto from a dict
asset_metadata_bulk_delete_dto_from_dict = AssetMetadataBulkDeleteDto.from_dict(asset_metadata_bulk_delete_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



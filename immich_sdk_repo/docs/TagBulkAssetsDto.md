# TagBulkAssetsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_ids** | **List[UUID]** | Asset IDs | 
**tag_ids** | **List[UUID]** | Tag IDs | 

## Example

```python
from immich_sdk.models.tag_bulk_assets_dto import TagBulkAssetsDto

# TODO update the JSON string below
json = "{}"
# create an instance of TagBulkAssetsDto from a JSON string
tag_bulk_assets_dto_instance = TagBulkAssetsDto.from_json(json)
# print the JSON string representation of the object
print(TagBulkAssetsDto.to_json())

# convert the object into a dict
tag_bulk_assets_dto_dict = tag_bulk_assets_dto_instance.to_dict()
# create an instance of TagBulkAssetsDto from a dict
tag_bulk_assets_dto_from_dict = TagBulkAssetsDto.from_dict(tag_bulk_assets_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



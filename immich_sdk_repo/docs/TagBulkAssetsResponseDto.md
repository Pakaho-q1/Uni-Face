# TagBulkAssetsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of assets tagged | 

## Example

```python
from immich_sdk.models.tag_bulk_assets_response_dto import TagBulkAssetsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of TagBulkAssetsResponseDto from a JSON string
tag_bulk_assets_response_dto_instance = TagBulkAssetsResponseDto.from_json(json)
# print the JSON string representation of the object
print(TagBulkAssetsResponseDto.to_json())

# convert the object into a dict
tag_bulk_assets_response_dto_dict = tag_bulk_assets_response_dto_instance.to_dict()
# create an instance of TagBulkAssetsResponseDto from a dict
tag_bulk_assets_response_dto_from_dict = TagBulkAssetsResponseDto.from_dict(tag_bulk_assets_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AlbumsAddAssetsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_ids** | **List[UUID]** | Album IDs | 
**asset_ids** | **List[UUID]** | Asset IDs | 

## Example

```python
from immich_sdk.models.albums_add_assets_dto import AlbumsAddAssetsDto

# TODO update the JSON string below
json = "{}"
# create an instance of AlbumsAddAssetsDto from a JSON string
albums_add_assets_dto_instance = AlbumsAddAssetsDto.from_json(json)
# print the JSON string representation of the object
print(AlbumsAddAssetsDto.to_json())

# convert the object into a dict
albums_add_assets_dto_dict = albums_add_assets_dto_instance.to_dict()
# create an instance of AlbumsAddAssetsDto from a dict
albums_add_assets_dto_from_dict = AlbumsAddAssetsDto.from_dict(albums_add_assets_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



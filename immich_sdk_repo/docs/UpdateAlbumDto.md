# UpdateAlbumDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_name** | **str** | Album name | [optional] 
**album_thumbnail_asset_id** | **UUID** | Album thumbnail asset ID | [optional] 
**description** | **str** | Album description | [optional] 
**is_activity_enabled** | **bool** | Enable activity feed | [optional] 
**order** | [**AssetOrder**](AssetOrder.md) |  | [optional] 

## Example

```python
from immich_sdk.models.update_album_dto import UpdateAlbumDto

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAlbumDto from a JSON string
update_album_dto_instance = UpdateAlbumDto.from_json(json)
# print the JSON string representation of the object
print(UpdateAlbumDto.to_json())

# convert the object into a dict
update_album_dto_dict = update_album_dto_instance.to_dict()
# create an instance of UpdateAlbumDto from a dict
update_album_dto_from_dict = UpdateAlbumDto.from_dict(update_album_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



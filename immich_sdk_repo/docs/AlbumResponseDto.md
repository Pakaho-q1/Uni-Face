# AlbumResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_name** | **str** | Album name | 
**album_thumbnail_asset_id** | **UUID** | Thumbnail asset ID | 
**album_users** | [**List[AlbumUserResponseDto]**](AlbumUserResponseDto.md) | First entry is always the album owner. Second entry is the auth user, if it differs from the owner. The rest are ordered alphabetically. | 
**asset_count** | **int** | Number of assets | 
**contributor_counts** | [**List[ContributorCountResponseDto]**](ContributorCountResponseDto.md) |  | [optional] 
**created_at** | **datetime** | Creation date | 
**description** | **str** | Album description | 
**end_date** | **datetime** | End date (latest asset) | [optional] 
**has_shared_link** | **bool** | Has shared link | 
**id** | **UUID** | Album ID | 
**is_activity_enabled** | **bool** | Activity feed enabled | 
**last_modified_asset_timestamp** | **datetime** | Last modified asset timestamp | [optional] 
**order** | [**AssetOrder**](AssetOrder.md) |  | [optional] 
**shared** | **bool** | Is shared album | 
**start_date** | **datetime** | Start date (earliest asset) | [optional] 
**updated_at** | **datetime** | Last update date | 

## Example

```python
from immich_sdk.models.album_response_dto import AlbumResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AlbumResponseDto from a JSON string
album_response_dto_instance = AlbumResponseDto.from_json(json)
# print the JSON string representation of the object
print(AlbumResponseDto.to_json())

# convert the object into a dict
album_response_dto_dict = album_response_dto_instance.to_dict()
# create an instance of AlbumResponseDto from a dict
album_response_dto_from_dict = AlbumResponseDto.from_dict(album_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



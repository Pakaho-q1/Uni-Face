# CreateAlbumDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_name** | **str** | Album name | 
**album_users** | [**List[AlbumUserCreateDto]**](AlbumUserCreateDto.md) | Album users | [optional] 
**asset_ids** | **List[UUID]** | Initial asset IDs | [optional] 
**description** | **str** | Album description | [optional] 

## Example

```python
from immich_sdk.models.create_album_dto import CreateAlbumDto

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAlbumDto from a JSON string
create_album_dto_instance = CreateAlbumDto.from_json(json)
# print the JSON string representation of the object
print(CreateAlbumDto.to_json())

# convert the object into a dict
create_album_dto_dict = create_album_dto_instance.to_dict()
# create an instance of CreateAlbumDto from a dict
create_album_dto_from_dict = CreateAlbumDto.from_dict(create_album_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



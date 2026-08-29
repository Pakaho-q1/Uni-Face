# AlbumsAddAssetsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**BulkIdErrorReason**](BulkIdErrorReason.md) |  | [optional] 
**success** | **bool** | Operation success | 

## Example

```python
from immich_sdk.models.albums_add_assets_response_dto import AlbumsAddAssetsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AlbumsAddAssetsResponseDto from a JSON string
albums_add_assets_response_dto_instance = AlbumsAddAssetsResponseDto.from_json(json)
# print the JSON string representation of the object
print(AlbumsAddAssetsResponseDto.to_json())

# convert the object into a dict
albums_add_assets_response_dto_dict = albums_add_assets_response_dto_instance.to_dict()
# create an instance of AlbumsAddAssetsResponseDto from a dict
albums_add_assets_response_dto_from_dict = AlbumsAddAssetsResponseDto.from_dict(albums_add_assets_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



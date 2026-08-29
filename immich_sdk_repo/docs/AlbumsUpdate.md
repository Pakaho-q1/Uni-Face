# AlbumsUpdate

Album preferences

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_asset_order** | [**AssetOrder**](AssetOrder.md) |  | [optional] 

## Example

```python
from immich_sdk.models.albums_update import AlbumsUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of AlbumsUpdate from a JSON string
albums_update_instance = AlbumsUpdate.from_json(json)
# print the JSON string representation of the object
print(AlbumsUpdate.to_json())

# convert the object into a dict
albums_update_dict = albums_update_instance.to_dict()
# create an instance of AlbumsUpdate from a dict
albums_update_from_dict = AlbumsUpdate.from_dict(albums_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



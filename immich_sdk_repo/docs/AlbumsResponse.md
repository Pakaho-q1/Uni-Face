# AlbumsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_asset_order** | [**AssetOrder**](AssetOrder.md) |  | 

## Example

```python
from immich_sdk.models.albums_response import AlbumsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AlbumsResponse from a JSON string
albums_response_instance = AlbumsResponse.from_json(json)
# print the JSON string representation of the object
print(AlbumsResponse.to_json())

# convert the object into a dict
albums_response_dict = albums_response_instance.to_dict()
# create an instance of AlbumsResponse from a dict
albums_response_from_dict = AlbumsResponse.from_dict(albums_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



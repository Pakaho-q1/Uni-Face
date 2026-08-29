# EnumFilterAssetVisibility


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | [**AssetVisibility**](AssetVisibility.md) |  | [optional] 
**var_in** | [**List[AssetVisibility]**](AssetVisibility.md) |  | [optional] 
**ne** | [**AssetVisibility**](AssetVisibility.md) |  | [optional] 
**not_in** | [**List[AssetVisibility]**](AssetVisibility.md) |  | [optional] 

## Example

```python
from immich_sdk.models.enum_filter_asset_visibility import EnumFilterAssetVisibility

# TODO update the JSON string below
json = "{}"
# create an instance of EnumFilterAssetVisibility from a JSON string
enum_filter_asset_visibility_instance = EnumFilterAssetVisibility.from_json(json)
# print the JSON string representation of the object
print(EnumFilterAssetVisibility.to_json())

# convert the object into a dict
enum_filter_asset_visibility_dict = enum_filter_asset_visibility_instance.to_dict()
# create an instance of EnumFilterAssetVisibility from a dict
enum_filter_asset_visibility_from_dict = EnumFilterAssetVisibility.from_dict(enum_filter_asset_visibility_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



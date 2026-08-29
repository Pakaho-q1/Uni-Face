# EnumFilterAssetType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eq** | [**AssetTypeEnum**](AssetTypeEnum.md) |  | [optional] 
**var_in** | [**List[AssetTypeEnum]**](AssetTypeEnum.md) |  | [optional] 
**ne** | [**AssetTypeEnum**](AssetTypeEnum.md) |  | [optional] 
**not_in** | [**List[AssetTypeEnum]**](AssetTypeEnum.md) |  | [optional] 

## Example

```python
from immich_sdk.models.enum_filter_asset_type import EnumFilterAssetType

# TODO update the JSON string below
json = "{}"
# create an instance of EnumFilterAssetType from a JSON string
enum_filter_asset_type_instance = EnumFilterAssetType.from_json(json)
# print the JSON string representation of the object
print(EnumFilterAssetType.to_json())

# convert the object into a dict
enum_filter_asset_type_dict = enum_filter_asset_type_instance.to_dict()
# create an instance of EnumFilterAssetType from a dict
enum_filter_asset_type_from_dict = EnumFilterAssetType.from_dict(enum_filter_asset_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



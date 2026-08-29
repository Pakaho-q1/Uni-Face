# AssetEditActionItemDtoParameters

List of edit actions to apply (crop, rotate, or mirror)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | **int** | Height of the crop | 
**width** | **int** | Width of the crop | 
**x** | **int** | Top-Left X coordinate of crop | 
**y** | **int** | Top-Left Y coordinate of crop | 
**angle** | **float** | Rotation angle in degrees | 
**axis** | [**MirrorAxis**](MirrorAxis.md) |  | 

## Example

```python
from immich_sdk.models.asset_edit_action_item_dto_parameters import AssetEditActionItemDtoParameters

# TODO update the JSON string below
json = "{}"
# create an instance of AssetEditActionItemDtoParameters from a JSON string
asset_edit_action_item_dto_parameters_instance = AssetEditActionItemDtoParameters.from_json(json)
# print the JSON string representation of the object
print(AssetEditActionItemDtoParameters.to_json())

# convert the object into a dict
asset_edit_action_item_dto_parameters_dict = asset_edit_action_item_dto_parameters_instance.to_dict()
# create an instance of AssetEditActionItemDtoParameters from a dict
asset_edit_action_item_dto_parameters_from_dict = AssetEditActionItemDtoParameters.from_dict(asset_edit_action_item_dto_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



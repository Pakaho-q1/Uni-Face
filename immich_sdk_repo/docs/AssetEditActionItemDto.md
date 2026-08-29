# AssetEditActionItemDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | [**AssetEditAction**](AssetEditAction.md) |  | 
**parameters** | [**AssetEditActionItemDtoParameters**](AssetEditActionItemDtoParameters.md) |  | 

## Example

```python
from immich_sdk.models.asset_edit_action_item_dto import AssetEditActionItemDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetEditActionItemDto from a JSON string
asset_edit_action_item_dto_instance = AssetEditActionItemDto.from_json(json)
# print the JSON string representation of the object
print(AssetEditActionItemDto.to_json())

# convert the object into a dict
asset_edit_action_item_dto_dict = asset_edit_action_item_dto_instance.to_dict()
# create an instance of AssetEditActionItemDto from a dict
asset_edit_action_item_dto_from_dict = AssetEditActionItemDto.from_dict(asset_edit_action_item_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AssetEditsCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**edits** | [**List[AssetEditActionItemDto]**](AssetEditActionItemDto.md) | List of edit actions to apply (crop, rotate, or mirror) | 

## Example

```python
from immich_sdk.models.asset_edits_create_dto import AssetEditsCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetEditsCreateDto from a JSON string
asset_edits_create_dto_instance = AssetEditsCreateDto.from_json(json)
# print the JSON string representation of the object
print(AssetEditsCreateDto.to_json())

# convert the object into a dict
asset_edits_create_dto_dict = asset_edits_create_dto_instance.to_dict()
# create an instance of AssetEditsCreateDto from a dict
asset_edits_create_dto_from_dict = AssetEditsCreateDto.from_dict(asset_edits_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



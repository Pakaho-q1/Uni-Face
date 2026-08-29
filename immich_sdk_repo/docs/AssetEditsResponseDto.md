# AssetEditsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID these edits belong to | 
**edits** | [**List[AssetEditActionItemResponseDto]**](AssetEditActionItemResponseDto.md) | List of edit actions applied to the asset | 

## Example

```python
from immich_sdk.models.asset_edits_response_dto import AssetEditsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetEditsResponseDto from a JSON string
asset_edits_response_dto_instance = AssetEditsResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetEditsResponseDto.to_json())

# convert the object into a dict
asset_edits_response_dto_dict = asset_edits_response_dto_instance.to_dict()
# create an instance of AssetEditsResponseDto from a dict
asset_edits_response_dto_from_dict = AssetEditsResponseDto.from_dict(asset_edits_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AssetStackResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_count** | **int** | Number of assets in stack | 
**id** | **UUID** | Stack ID | 
**primary_asset_id** | **UUID** | Primary asset ID | 

## Example

```python
from immich_sdk.models.asset_stack_response_dto import AssetStackResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetStackResponseDto from a JSON string
asset_stack_response_dto_instance = AssetStackResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetStackResponseDto.to_json())

# convert the object into a dict
asset_stack_response_dto_dict = asset_stack_response_dto_instance.to_dict()
# create an instance of AssetStackResponseDto from a dict
asset_stack_response_dto_from_dict = AssetStackResponseDto.from_dict(asset_stack_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



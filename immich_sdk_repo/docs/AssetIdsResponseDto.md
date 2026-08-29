# AssetIdsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**error** | [**AssetIdErrorReason**](AssetIdErrorReason.md) |  | [optional] 
**success** | **bool** | Whether operation succeeded | 

## Example

```python
from immich_sdk.models.asset_ids_response_dto import AssetIdsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetIdsResponseDto from a JSON string
asset_ids_response_dto_instance = AssetIdsResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetIdsResponseDto.to_json())

# convert the object into a dict
asset_ids_response_dto_dict = asset_ids_response_dto_instance.to_dict()
# create an instance of AssetIdsResponseDto from a dict
asset_ids_response_dto_from_dict = AssetIdsResponseDto.from_dict(asset_ids_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



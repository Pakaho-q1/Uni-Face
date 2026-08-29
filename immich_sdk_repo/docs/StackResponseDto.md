# StackResponseDto

Stack response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assets** | [**List[AssetResponseDto]**](AssetResponseDto.md) |  | 
**id** | **UUID** | Stack ID | 
**primary_asset_id** | **UUID** | Primary asset ID | 

## Example

```python
from immich_sdk.models.stack_response_dto import StackResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of StackResponseDto from a JSON string
stack_response_dto_instance = StackResponseDto.from_json(json)
# print the JSON string representation of the object
print(StackResponseDto.to_json())

# convert the object into a dict
stack_response_dto_dict = stack_response_dto_instance.to_dict()
# create an instance of StackResponseDto from a dict
stack_response_dto_from_dict = StackResponseDto.from_dict(stack_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



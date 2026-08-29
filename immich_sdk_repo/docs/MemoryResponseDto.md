# MemoryResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assets** | [**List[AssetResponseDto]**](AssetResponseDto.md) |  | 
**created_at** | **datetime** | Creation date | 
**data** | [**OnThisDayDto**](OnThisDayDto.md) |  | 
**deleted_at** | **datetime** | Deletion date | [optional] 
**hide_at** | **datetime** | Date when memory should be hidden | [optional] 
**id** | **UUID** | Memory ID | 
**is_saved** | **bool** | Is memory saved | 
**memory_at** | **datetime** | Memory date | 
**owner_id** | **UUID** | Owner user ID | 
**seen_at** | **datetime** | Date when memory was seen | [optional] 
**show_at** | **datetime** | Date when memory should be shown | [optional] 
**type** | [**MemoryType**](MemoryType.md) |  | 
**updated_at** | **datetime** | Last update date | 

## Example

```python
from immich_sdk.models.memory_response_dto import MemoryResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryResponseDto from a JSON string
memory_response_dto_instance = MemoryResponseDto.from_json(json)
# print the JSON string representation of the object
print(MemoryResponseDto.to_json())

# convert the object into a dict
memory_response_dto_dict = memory_response_dto_instance.to_dict()
# create an instance of MemoryResponseDto from a dict
memory_response_dto_from_dict = MemoryResponseDto.from_dict(memory_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



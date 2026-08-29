# MemoryCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_ids** | **List[UUID]** | Asset IDs to associate with memory | [optional] 
**data** | [**OnThisDayDto**](OnThisDayDto.md) |  | 
**hide_at** | **datetime** | Date when memory should be hidden | [optional] 
**is_saved** | **bool** | Is memory saved | [optional] 
**memory_at** | **datetime** | Memory date | 
**seen_at** | **datetime** | Date when memory was seen | [optional] 
**show_at** | **datetime** | Date when memory should be shown | [optional] 
**type** | [**MemoryType**](MemoryType.md) |  | 

## Example

```python
from immich_sdk.models.memory_create_dto import MemoryCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryCreateDto from a JSON string
memory_create_dto_instance = MemoryCreateDto.from_json(json)
# print the JSON string representation of the object
print(MemoryCreateDto.to_json())

# convert the object into a dict
memory_create_dto_dict = memory_create_dto_instance.to_dict()
# create an instance of MemoryCreateDto from a dict
memory_create_dto_from_dict = MemoryCreateDto.from_dict(memory_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



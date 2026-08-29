# MemoryStatisticsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Total number of memories | 

## Example

```python
from immich_sdk.models.memory_statistics_response_dto import MemoryStatisticsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of MemoryStatisticsResponseDto from a JSON string
memory_statistics_response_dto_instance = MemoryStatisticsResponseDto.from_json(json)
# print the JSON string representation of the object
print(MemoryStatisticsResponseDto.to_json())

# convert the object into a dict
memory_statistics_response_dto_dict = memory_statistics_response_dto_instance.to_dict()
# create an instance of MemoryStatisticsResponseDto from a dict
memory_statistics_response_dto_from_dict = MemoryStatisticsResponseDto.from_dict(memory_statistics_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# QueueStatisticsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active** | **int** | Number of active jobs | 
**completed** | **int** | Number of completed jobs | 
**delayed** | **int** | Number of delayed jobs | 
**failed** | **int** | Number of failed jobs | 
**paused** | **int** | Number of paused jobs | 
**waiting** | **int** | Number of waiting jobs | 

## Example

```python
from immich_sdk.models.queue_statistics_dto import QueueStatisticsDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueStatisticsDto from a JSON string
queue_statistics_dto_instance = QueueStatisticsDto.from_json(json)
# print the JSON string representation of the object
print(QueueStatisticsDto.to_json())

# convert the object into a dict
queue_statistics_dto_dict = queue_statistics_dto_instance.to_dict()
# create an instance of QueueStatisticsDto from a dict
queue_statistics_dto_from_dict = QueueStatisticsDto.from_dict(queue_statistics_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



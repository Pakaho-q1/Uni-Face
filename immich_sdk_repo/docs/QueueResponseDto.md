# QueueResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_paused** | **bool** | Whether the queue is paused | 
**name** | [**QueueName**](QueueName.md) |  | 
**statistics** | [**QueueStatisticsDto**](QueueStatisticsDto.md) |  | 

## Example

```python
from immich_sdk.models.queue_response_dto import QueueResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueResponseDto from a JSON string
queue_response_dto_instance = QueueResponseDto.from_json(json)
# print the JSON string representation of the object
print(QueueResponseDto.to_json())

# convert the object into a dict
queue_response_dto_dict = queue_response_dto_instance.to_dict()
# create an instance of QueueResponseDto from a dict
queue_response_dto_from_dict = QueueResponseDto.from_dict(queue_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# QueueResponseLegacyDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_counts** | [**QueueStatisticsDto**](QueueStatisticsDto.md) |  | 
**queue_status** | [**QueueStatusLegacyDto**](QueueStatusLegacyDto.md) |  | 

## Example

```python
from immich_sdk.models.queue_response_legacy_dto import QueueResponseLegacyDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueResponseLegacyDto from a JSON string
queue_response_legacy_dto_instance = QueueResponseLegacyDto.from_json(json)
# print the JSON string representation of the object
print(QueueResponseLegacyDto.to_json())

# convert the object into a dict
queue_response_legacy_dto_dict = queue_response_legacy_dto_instance.to_dict()
# create an instance of QueueResponseLegacyDto from a dict
queue_response_legacy_dto_from_dict = QueueResponseLegacyDto.from_dict(queue_response_legacy_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



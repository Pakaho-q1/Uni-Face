# QueueStatusLegacyDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_active** | **bool** | Whether the queue is currently active (has running jobs) | 
**is_paused** | **bool** | Whether the queue is paused | 

## Example

```python
from immich_sdk.models.queue_status_legacy_dto import QueueStatusLegacyDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueStatusLegacyDto from a JSON string
queue_status_legacy_dto_instance = QueueStatusLegacyDto.from_json(json)
# print the JSON string representation of the object
print(QueueStatusLegacyDto.to_json())

# convert the object into a dict
queue_status_legacy_dto_dict = queue_status_legacy_dto_instance.to_dict()
# create an instance of QueueStatusLegacyDto from a dict
queue_status_legacy_dto_from_dict = QueueStatusLegacyDto.from_dict(queue_status_legacy_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



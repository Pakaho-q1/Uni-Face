# QueueDeleteDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**failed** | **bool** | If true, will also remove failed jobs from the queue. | [optional] 

## Example

```python
from immich_sdk.models.queue_delete_dto import QueueDeleteDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueDeleteDto from a JSON string
queue_delete_dto_instance = QueueDeleteDto.from_json(json)
# print the JSON string representation of the object
print(QueueDeleteDto.to_json())

# convert the object into a dict
queue_delete_dto_dict = queue_delete_dto_instance.to_dict()
# create an instance of QueueDeleteDto from a dict
queue_delete_dto_from_dict = QueueDeleteDto.from_dict(queue_delete_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# QueueUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_paused** | **bool** | Whether to pause the queue | [optional] 

## Example

```python
from immich_sdk.models.queue_update_dto import QueueUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueUpdateDto from a JSON string
queue_update_dto_instance = QueueUpdateDto.from_json(json)
# print the JSON string representation of the object
print(QueueUpdateDto.to_json())

# convert the object into a dict
queue_update_dto_dict = queue_update_dto_instance.to_dict()
# create an instance of QueueUpdateDto from a dict
queue_update_dto_from_dict = QueueUpdateDto.from_dict(queue_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



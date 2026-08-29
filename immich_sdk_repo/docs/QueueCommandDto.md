# QueueCommandDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**command** | [**QueueCommand**](QueueCommand.md) |  | 
**force** | **bool** | Force the command execution (if applicable) | [optional] 

## Example

```python
from immich_sdk.models.queue_command_dto import QueueCommandDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueCommandDto from a JSON string
queue_command_dto_instance = QueueCommandDto.from_json(json)
# print the JSON string representation of the object
print(QueueCommandDto.to_json())

# convert the object into a dict
queue_command_dto_dict = queue_command_dto_instance.to_dict()
# create an instance of QueueCommandDto from a dict
queue_command_dto_from_dict = QueueCommandDto.from_dict(queue_command_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# QueueJobResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **Dict[str, object]** | Job data payload | 
**id** | **str** | Job ID | [optional] 
**name** | [**JobName**](JobName.md) |  | 
**timestamp** | **int** | Job creation timestamp | 

## Example

```python
from immich_sdk.models.queue_job_response_dto import QueueJobResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueueJobResponseDto from a JSON string
queue_job_response_dto_instance = QueueJobResponseDto.from_json(json)
# print the JSON string representation of the object
print(QueueJobResponseDto.to_json())

# convert the object into a dict
queue_job_response_dto_dict = queue_job_response_dto_instance.to_dict()
# create an instance of QueueJobResponseDto from a dict
queue_job_response_dto_from_dict = QueueJobResponseDto.from_dict(queue_job_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



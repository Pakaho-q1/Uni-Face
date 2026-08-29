# WorkflowTriggerResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trigger** | [**WorkflowTrigger**](WorkflowTrigger.md) |  | 
**types** | [**List[WorkflowType]**](WorkflowType.md) | Workflow types | 

## Example

```python
from immich_sdk.models.workflow_trigger_response_dto import WorkflowTriggerResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowTriggerResponseDto from a JSON string
workflow_trigger_response_dto_instance = WorkflowTriggerResponseDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowTriggerResponseDto.to_json())

# convert the object into a dict
workflow_trigger_response_dto_dict = workflow_trigger_response_dto_instance.to_dict()
# create an instance of WorkflowTriggerResponseDto from a dict
workflow_trigger_response_dto_from_dict = WorkflowTriggerResponseDto.from_dict(workflow_trigger_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



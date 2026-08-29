# WorkflowResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **str** | Creation date | 
**description** | **str** | Workflow description | 
**enabled** | **bool** | Workflow enabled | 
**id** | **UUID** | Workflow ID | 
**logging** | **bool** | Workflow logs run results | 
**name** | **str** | Workflow name | 
**steps** | [**List[WorkflowStepDto]**](WorkflowStepDto.md) | Workflow steps | 
**trigger** | [**WorkflowTrigger**](WorkflowTrigger.md) |  | 
**updated_at** | **str** | Update date | 

## Example

```python
from immich_sdk.models.workflow_response_dto import WorkflowResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowResponseDto from a JSON string
workflow_response_dto_instance = WorkflowResponseDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowResponseDto.to_json())

# convert the object into a dict
workflow_response_dto_dict = workflow_response_dto_instance.to_dict()
# create an instance of WorkflowResponseDto from a dict
workflow_response_dto_from_dict = WorkflowResponseDto.from_dict(workflow_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



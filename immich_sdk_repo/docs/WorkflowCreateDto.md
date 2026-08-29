# WorkflowCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Workflow description | [optional] 
**enabled** | **bool** | Workflow enabled | [optional] 
**logging** | **bool** | Workflow logs run results | [optional] 
**name** | **str** | Workflow name | [optional] 
**steps** | [**List[WorkflowStepDto]**](WorkflowStepDto.md) |  | [optional] 
**trigger** | [**WorkflowTrigger**](WorkflowTrigger.md) |  | 

## Example

```python
from immich_sdk.models.workflow_create_dto import WorkflowCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowCreateDto from a JSON string
workflow_create_dto_instance = WorkflowCreateDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowCreateDto.to_json())

# convert the object into a dict
workflow_create_dto_dict = workflow_create_dto_instance.to_dict()
# create an instance of WorkflowCreateDto from a dict
workflow_create_dto_from_dict = WorkflowCreateDto.from_dict(workflow_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



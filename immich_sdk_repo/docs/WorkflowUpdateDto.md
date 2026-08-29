# WorkflowUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Workflow description | [optional] 
**enabled** | **bool** | Workflow enabled | [optional] 
**logging** | **bool** | Workflow logs run results | [optional] 
**name** | **str** | Workflow name | [optional] 
**steps** | [**List[WorkflowStepDto]**](WorkflowStepDto.md) |  | [optional] 
**trigger** | [**WorkflowTrigger**](WorkflowTrigger.md) |  | [optional] 

## Example

```python
from immich_sdk.models.workflow_update_dto import WorkflowUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowUpdateDto from a JSON string
workflow_update_dto_instance = WorkflowUpdateDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowUpdateDto.to_json())

# convert the object into a dict
workflow_update_dto_dict = workflow_update_dto_instance.to_dict()
# create an instance of WorkflowUpdateDto from a dict
workflow_update_dto_from_dict = WorkflowUpdateDto.from_dict(workflow_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



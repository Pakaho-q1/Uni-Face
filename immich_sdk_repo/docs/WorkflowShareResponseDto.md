# WorkflowShareResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Workflow description | 
**name** | **str** | Workflow name | 
**steps** | [**List[WorkflowShareStepDto]**](WorkflowShareStepDto.md) | Workflow steps | 
**trigger** | [**WorkflowTrigger**](WorkflowTrigger.md) |  | 

## Example

```python
from immich_sdk.models.workflow_share_response_dto import WorkflowShareResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowShareResponseDto from a JSON string
workflow_share_response_dto_instance = WorkflowShareResponseDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowShareResponseDto.to_json())

# convert the object into a dict
workflow_share_response_dto_dict = workflow_share_response_dto_instance.to_dict()
# create an instance of WorkflowShareResponseDto from a dict
workflow_share_response_dto_from_dict = WorkflowShareResponseDto.from_dict(workflow_share_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



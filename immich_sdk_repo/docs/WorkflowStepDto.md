# WorkflowStepDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **Dict[str, object]** | Step configuration | 
**enabled** | **bool** | Step is enabled | [optional] 
**method** | **str** | Step plugin method | 

## Example

```python
from immich_sdk.models.workflow_step_dto import WorkflowStepDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowStepDto from a JSON string
workflow_step_dto_instance = WorkflowStepDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowStepDto.to_json())

# convert the object into a dict
workflow_step_dto_dict = workflow_step_dto_instance.to_dict()
# create an instance of WorkflowStepDto from a dict
workflow_step_dto_from_dict = WorkflowStepDto.from_dict(workflow_step_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



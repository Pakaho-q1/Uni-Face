# WorkflowLogEntryDtoLastStep

Last step ran, if the workflow ended early

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **int** | Index of the step in the workflow | 
**method** | **str** | Method of the step | 

## Example

```python
from immich_sdk.models.workflow_log_entry_dto_last_step import WorkflowLogEntryDtoLastStep

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowLogEntryDtoLastStep from a JSON string
workflow_log_entry_dto_last_step_instance = WorkflowLogEntryDtoLastStep.from_json(json)
# print the JSON string representation of the object
print(WorkflowLogEntryDtoLastStep.to_json())

# convert the object into a dict
workflow_log_entry_dto_last_step_dict = workflow_log_entry_dto_last_step_instance.to_dict()
# create an instance of WorkflowLogEntryDtoLastStep from a dict
workflow_log_entry_dto_last_step_from_dict = WorkflowLogEntryDtoLastStep.from_dict(workflow_log_entry_dto_last_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



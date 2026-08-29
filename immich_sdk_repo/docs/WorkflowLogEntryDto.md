# WorkflowLogEntryDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**at** | **datetime** | Workflow run date/time | 
**id** | **UUID** | Workflow log entry ID | 
**last_step** | [**WorkflowLogEntryDtoLastStep**](WorkflowLogEntryDtoLastStep.md) |  | [optional] 
**result** | [**WorkflowResult**](WorkflowResult.md) |  | 
**trigger_data_id** | **UUID** | Workflow trigger data ID | [optional] 

## Example

```python
from immich_sdk.models.workflow_log_entry_dto import WorkflowLogEntryDto

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowLogEntryDto from a JSON string
workflow_log_entry_dto_instance = WorkflowLogEntryDto.from_json(json)
# print the JSON string representation of the object
print(WorkflowLogEntryDto.to_json())

# convert the object into a dict
workflow_log_entry_dto_dict = workflow_log_entry_dto_instance.to_dict()
# create an instance of WorkflowLogEntryDto from a dict
workflow_log_entry_dto_from_dict = WorkflowLogEntryDto.from_dict(workflow_log_entry_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



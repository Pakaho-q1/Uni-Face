# PluginTemplateResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Template description | 
**key** | **str** | Template key (unique across all templates) | 
**steps** | [**List[PluginTemplateStepResponseDto]**](PluginTemplateStepResponseDto.md) | Workflow steps | 
**title** | **str** | Template title | 
**trigger** | [**WorkflowTrigger**](WorkflowTrigger.md) |  | 
**ui_hints** | **List[str]** | Ui hints, for example \&quot;smart-album\&quot; | 

## Example

```python
from immich_sdk.models.plugin_template_response_dto import PluginTemplateResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of PluginTemplateResponseDto from a JSON string
plugin_template_response_dto_instance = PluginTemplateResponseDto.from_json(json)
# print the JSON string representation of the object
print(PluginTemplateResponseDto.to_json())

# convert the object into a dict
plugin_template_response_dto_dict = plugin_template_response_dto_instance.to_dict()
# create an instance of PluginTemplateResponseDto from a dict
plugin_template_response_dto_from_dict = PluginTemplateResponseDto.from_dict(plugin_template_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



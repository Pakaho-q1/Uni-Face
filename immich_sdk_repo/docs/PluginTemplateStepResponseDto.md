# PluginTemplateStepResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **Dict[str, object]** | Step configuration | 
**enabled** | **bool** | Whether the step is enabled | [optional] 
**method** | **str** | Step plugin method | 

## Example

```python
from immich_sdk.models.plugin_template_step_response_dto import PluginTemplateStepResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of PluginTemplateStepResponseDto from a JSON string
plugin_template_step_response_dto_instance = PluginTemplateStepResponseDto.from_json(json)
# print the JSON string representation of the object
print(PluginTemplateStepResponseDto.to_json())

# convert the object into a dict
plugin_template_step_response_dto_dict = plugin_template_step_response_dto_instance.to_dict()
# create an instance of PluginTemplateStepResponseDto from a dict
plugin_template_step_response_dto_from_dict = PluginTemplateStepResponseDto.from_dict(plugin_template_step_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



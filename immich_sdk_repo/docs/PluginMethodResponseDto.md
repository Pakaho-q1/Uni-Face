# PluginMethodResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Description | 
**host_functions** | **bool** |  | 
**key** | **str** | Key | 
**name** | **str** | Name | 
**var_schema** | **object** |  | [optional] 
**title** | **str** | Title | 
**types** | [**List[WorkflowType]**](WorkflowType.md) | Workflow types | 
**ui_hints** | **List[str]** | Ui hints | 

## Example

```python
from immich_sdk.models.plugin_method_response_dto import PluginMethodResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of PluginMethodResponseDto from a JSON string
plugin_method_response_dto_instance = PluginMethodResponseDto.from_json(json)
# print the JSON string representation of the object
print(PluginMethodResponseDto.to_json())

# convert the object into a dict
plugin_method_response_dto_dict = plugin_method_response_dto_instance.to_dict()
# create an instance of PluginMethodResponseDto from a dict
plugin_method_response_dto_from_dict = PluginMethodResponseDto.from_dict(plugin_method_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



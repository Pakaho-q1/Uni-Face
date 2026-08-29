# PluginResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author** | **str** | Plugin author | 
**created_at** | **str** | Creation date | 
**description** | **str** | Plugin description | 
**id** | **UUID** | Plugin ID | 
**methods** | [**List[PluginMethodResponseDto]**](PluginMethodResponseDto.md) | Plugin methods | 
**name** | **str** | Plugin name | 
**title** | **str** | Plugin title | 
**updated_at** | **str** | Last update date | 
**version** | **str** | Plugin version | 

## Example

```python
from immich_sdk.models.plugin_response_dto import PluginResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of PluginResponseDto from a JSON string
plugin_response_dto_instance = PluginResponseDto.from_json(json)
# print the JSON string representation of the object
print(PluginResponseDto.to_json())

# convert the object into a dict
plugin_response_dto_dict = plugin_response_dto_instance.to_dict()
# create an instance of PluginResponseDto from a dict
plugin_response_dto_from_dict = PluginResponseDto.from_dict(plugin_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



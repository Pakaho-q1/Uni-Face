# SystemConfigTemplateStorageOptionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**day_options** | **List[str]** | Available day format options for storage template | 
**hour_options** | **List[str]** | Available hour format options for storage template | 
**minute_options** | **List[str]** | Available minute format options for storage template | 
**month_options** | **List[str]** | Available month format options for storage template | 
**preset_options** | **List[str]** | Available preset template options | 
**second_options** | **List[str]** | Available second format options for storage template | 
**week_options** | **List[str]** | Available week format options for storage template | 
**year_options** | **List[str]** | Available year format options for storage template | 

## Example

```python
from immich_sdk.models.system_config_template_storage_option_dto import SystemConfigTemplateStorageOptionDto

# TODO update the JSON string below
json = "{}"
# create an instance of SystemConfigTemplateStorageOptionDto from a JSON string
system_config_template_storage_option_dto_instance = SystemConfigTemplateStorageOptionDto.from_json(json)
# print the JSON string representation of the object
print(SystemConfigTemplateStorageOptionDto.to_json())

# convert the object into a dict
system_config_template_storage_option_dto_dict = system_config_template_storage_option_dto_instance.to_dict()
# create an instance of SystemConfigTemplateStorageOptionDto from a dict
system_config_template_storage_option_dto_from_dict = SystemConfigTemplateStorageOptionDto.from_dict(system_config_template_storage_option_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



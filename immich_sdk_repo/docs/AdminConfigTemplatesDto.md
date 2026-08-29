# AdminConfigTemplatesDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | [**AdminConfigTemplateEmailsDto**](AdminConfigTemplateEmailsDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_templates_dto import AdminConfigTemplatesDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigTemplatesDto from a JSON string
admin_config_templates_dto_instance = AdminConfigTemplatesDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigTemplatesDto.to_json())

# convert the object into a dict
admin_config_templates_dto_dict = admin_config_templates_dto_instance.to_dict()
# create an instance of AdminConfigTemplatesDto from a dict
admin_config_templates_dto_from_dict = AdminConfigTemplatesDto.from_dict(admin_config_templates_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



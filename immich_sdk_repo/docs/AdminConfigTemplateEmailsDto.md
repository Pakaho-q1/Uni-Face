# AdminConfigTemplateEmailsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_invite_template** | **str** | Album invite template | 
**album_update_template** | **str** | Album update template | 
**welcome_template** | **str** | Welcome template | 

## Example

```python
from immich_sdk.models.admin_config_template_emails_dto import AdminConfigTemplateEmailsDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigTemplateEmailsDto from a JSON string
admin_config_template_emails_dto_instance = AdminConfigTemplateEmailsDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigTemplateEmailsDto.to_json())

# convert the object into a dict
admin_config_template_emails_dto_dict = admin_config_template_emails_dto_instance.to_dict()
# create an instance of AdminConfigTemplateEmailsDto from a dict
admin_config_template_emails_dto_from_dict = AdminConfigTemplateEmailsDto.from_dict(admin_config_template_emails_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



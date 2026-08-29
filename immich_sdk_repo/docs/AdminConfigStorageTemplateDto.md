# AdminConfigStorageTemplateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 
**hash_verification_enabled** | **bool** | Hash verification enabled | 
**template** | **str** | Template | 

## Example

```python
from immich_sdk.models.admin_config_storage_template_dto import AdminConfigStorageTemplateDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigStorageTemplateDto from a JSON string
admin_config_storage_template_dto_instance = AdminConfigStorageTemplateDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigStorageTemplateDto.to_json())

# convert the object into a dict
admin_config_storage_template_dto_dict = admin_config_storage_template_dto_instance.to_dict()
# create an instance of AdminConfigStorageTemplateDto from a dict
admin_config_storage_template_dto_from_dict = AdminConfigStorageTemplateDto.from_dict(admin_config_storage_template_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



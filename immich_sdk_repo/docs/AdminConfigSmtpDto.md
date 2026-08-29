# AdminConfigSmtpDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether SMTP email notifications are enabled | 
**var_from** | **str** | Email address to send from | 
**reply_to** | **str** | Email address for replies | 
**transport** | [**AdminConfigSmtpTransportDto**](AdminConfigSmtpTransportDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_smtp_dto import AdminConfigSmtpDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigSmtpDto from a JSON string
admin_config_smtp_dto_instance = AdminConfigSmtpDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigSmtpDto.to_json())

# convert the object into a dict
admin_config_smtp_dto_dict = admin_config_smtp_dto_instance.to_dict()
# create an instance of AdminConfigSmtpDto from a dict
admin_config_smtp_dto_from_dict = AdminConfigSmtpDto.from_dict(admin_config_smtp_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



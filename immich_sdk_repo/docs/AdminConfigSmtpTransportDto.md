# AdminConfigSmtpTransportDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**host** | **str** | SMTP server hostname | 
**ignore_cert** | **bool** | Whether to ignore SSL certificate errors | 
**password** | **str** | SMTP password | 
**port** | **int** | SMTP server port | 
**secure** | **bool** | Whether to use secure connection (TLS/SSL) | 
**username** | **str** | SMTP username | 

## Example

```python
from immich_sdk.models.admin_config_smtp_transport_dto import AdminConfigSmtpTransportDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigSmtpTransportDto from a JSON string
admin_config_smtp_transport_dto_instance = AdminConfigSmtpTransportDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigSmtpTransportDto.to_json())

# convert the object into a dict
admin_config_smtp_transport_dto_dict = admin_config_smtp_transport_dto_instance.to_dict()
# create an instance of AdminConfigSmtpTransportDto from a dict
admin_config_smtp_transport_dto_from_dict = AdminConfigSmtpTransportDto.from_dict(admin_config_smtp_transport_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



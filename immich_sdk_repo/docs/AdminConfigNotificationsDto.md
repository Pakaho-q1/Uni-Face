# AdminConfigNotificationsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**smtp** | [**AdminConfigSmtpDto**](AdminConfigSmtpDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_notifications_dto import AdminConfigNotificationsDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigNotificationsDto from a JSON string
admin_config_notifications_dto_instance = AdminConfigNotificationsDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigNotificationsDto.to_json())

# convert the object into a dict
admin_config_notifications_dto_dict = admin_config_notifications_dto_instance.to_dict()
# create an instance of AdminConfigNotificationsDto from a dict
admin_config_notifications_dto_from_dict = AdminConfigNotificationsDto.from_dict(admin_config_notifications_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# NotificationCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **Dict[str, object]** | Additional notification data | [optional] 
**description** | **str** | Notification description | [optional] 
**level** | [**NotificationLevel**](NotificationLevel.md) |  | [optional] 
**read_at** | **datetime** | Date when notification was read | [optional] 
**title** | **str** | Notification title | 
**type** | [**NotificationType**](NotificationType.md) |  | [optional] 
**user_id** | **UUID** | User ID to send notification to | 

## Example

```python
from immich_sdk.models.notification_create_dto import NotificationCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationCreateDto from a JSON string
notification_create_dto_instance = NotificationCreateDto.from_json(json)
# print the JSON string representation of the object
print(NotificationCreateDto.to_json())

# convert the object into a dict
notification_create_dto_dict = notification_create_dto_instance.to_dict()
# create an instance of NotificationCreateDto from a dict
notification_create_dto_from_dict = NotificationCreateDto.from_dict(notification_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



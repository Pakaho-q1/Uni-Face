# NotificationUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**read_at** | **datetime** | Date when notification was read | [optional] 

## Example

```python
from immich_sdk.models.notification_update_dto import NotificationUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationUpdateDto from a JSON string
notification_update_dto_instance = NotificationUpdateDto.from_json(json)
# print the JSON string representation of the object
print(NotificationUpdateDto.to_json())

# convert the object into a dict
notification_update_dto_dict = notification_update_dto_instance.to_dict()
# create an instance of NotificationUpdateDto from a dict
notification_update_dto_from_dict = NotificationUpdateDto.from_dict(notification_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# NotificationUpdateAllDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ids** | **List[UUID]** | Notification IDs to update | 
**read_at** | **datetime** | Date when notifications were read | [optional] 

## Example

```python
from immich_sdk.models.notification_update_all_dto import NotificationUpdateAllDto

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationUpdateAllDto from a JSON string
notification_update_all_dto_instance = NotificationUpdateAllDto.from_json(json)
# print the JSON string representation of the object
print(NotificationUpdateAllDto.to_json())

# convert the object into a dict
notification_update_all_dto_dict = notification_update_all_dto_instance.to_dict()
# create an instance of NotificationUpdateAllDto from a dict
notification_update_all_dto_from_dict = NotificationUpdateAllDto.from_dict(notification_update_all_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



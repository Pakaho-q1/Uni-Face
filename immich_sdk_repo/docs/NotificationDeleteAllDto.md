# NotificationDeleteAllDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ids** | **List[UUID]** | Notification IDs to delete | 

## Example

```python
from immich_sdk.models.notification_delete_all_dto import NotificationDeleteAllDto

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationDeleteAllDto from a JSON string
notification_delete_all_dto_instance = NotificationDeleteAllDto.from_json(json)
# print the JSON string representation of the object
print(NotificationDeleteAllDto.to_json())

# convert the object into a dict
notification_delete_all_dto_dict = notification_delete_all_dto_instance.to_dict()
# create an instance of NotificationDeleteAllDto from a dict
notification_delete_all_dto_from_dict = NotificationDeleteAllDto.from_dict(notification_delete_all_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



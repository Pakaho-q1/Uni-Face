# UserPreferencesUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**albums** | [**AlbumsUpdate**](AlbumsUpdate.md) |  | [optional] 
**avatar** | [**AvatarUpdate**](AvatarUpdate.md) |  | [optional] 
**cast** | [**CastUpdate**](CastUpdate.md) |  | [optional] 
**download** | [**DownloadUpdate**](DownloadUpdate.md) |  | [optional] 
**email_notifications** | [**EmailNotificationsUpdate**](EmailNotificationsUpdate.md) |  | [optional] 
**folders** | [**FoldersUpdate**](FoldersUpdate.md) |  | [optional] 
**memories** | [**MemoriesUpdate**](MemoriesUpdate.md) |  | [optional] 
**people** | [**PeopleUpdate**](PeopleUpdate.md) |  | [optional] 
**purchase** | [**PurchaseUpdate**](PurchaseUpdate.md) |  | [optional] 
**ratings** | [**RatingsUpdate**](RatingsUpdate.md) |  | [optional] 
**recently_added** | [**RecentlyAddedUpdate**](RecentlyAddedUpdate.md) |  | [optional] 
**shared_links** | [**SharedLinksUpdate**](SharedLinksUpdate.md) |  | [optional] 
**tags** | [**TagsUpdate**](TagsUpdate.md) |  | [optional] 

## Example

```python
from immich_sdk.models.user_preferences_update_dto import UserPreferencesUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserPreferencesUpdateDto from a JSON string
user_preferences_update_dto_instance = UserPreferencesUpdateDto.from_json(json)
# print the JSON string representation of the object
print(UserPreferencesUpdateDto.to_json())

# convert the object into a dict
user_preferences_update_dto_dict = user_preferences_update_dto_instance.to_dict()
# create an instance of UserPreferencesUpdateDto from a dict
user_preferences_update_dto_from_dict = UserPreferencesUpdateDto.from_dict(user_preferences_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



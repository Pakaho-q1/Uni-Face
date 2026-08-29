# UserPreferencesResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**albums** | [**AlbumsResponse**](AlbumsResponse.md) |  | 
**cast** | [**CastResponse**](CastResponse.md) |  | 
**download** | [**DownloadResponse**](DownloadResponse.md) |  | 
**email_notifications** | [**EmailNotificationsResponse**](EmailNotificationsResponse.md) |  | 
**folders** | [**FoldersResponse**](FoldersResponse.md) |  | 
**memories** | [**MemoriesResponse**](MemoriesResponse.md) |  | 
**people** | [**PeopleResponse**](PeopleResponse.md) |  | 
**purchase** | [**PurchaseResponse**](PurchaseResponse.md) |  | 
**ratings** | [**RatingsResponse**](RatingsResponse.md) |  | 
**recently_added** | [**RecentlyAddedResponse**](RecentlyAddedResponse.md) |  | 
**shared_links** | [**SharedLinksResponse**](SharedLinksResponse.md) |  | 
**tags** | [**TagsResponse**](TagsResponse.md) |  | 

## Example

```python
from immich_sdk.models.user_preferences_response_dto import UserPreferencesResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserPreferencesResponseDto from a JSON string
user_preferences_response_dto_instance = UserPreferencesResponseDto.from_json(json)
# print the JSON string representation of the object
print(UserPreferencesResponseDto.to_json())

# convert the object into a dict
user_preferences_response_dto_dict = user_preferences_response_dto_instance.to_dict()
# create an instance of UserPreferencesResponseDto from a dict
user_preferences_response_dto_from_dict = UserPreferencesResponseDto.from_dict(user_preferences_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



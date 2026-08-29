# UsageByUserDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**photos** | **int** | Number of photos | 
**quota_size_in_bytes** | **int** | User quota size in bytes (null if unlimited) | 
**usage** | **int** | Total storage usage in bytes | 
**usage_photos** | **int** | Storage usage for photos in bytes | 
**usage_videos** | **int** | Storage usage for videos in bytes | 
**user_id** | **UUID** | User ID | 
**user_name** | **str** | User name | 
**videos** | **int** | Number of videos | 

## Example

```python
from immich_sdk.models.usage_by_user_dto import UsageByUserDto

# TODO update the JSON string below
json = "{}"
# create an instance of UsageByUserDto from a JSON string
usage_by_user_dto_instance = UsageByUserDto.from_json(json)
# print the JSON string representation of the object
print(UsageByUserDto.to_json())

# convert the object into a dict
usage_by_user_dto_dict = usage_by_user_dto_instance.to_dict()
# create an instance of UsageByUserDto from a dict
usage_by_user_dto_from_dict = UsageByUserDto.from_dict(usage_by_user_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



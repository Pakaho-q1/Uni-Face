# ServerStatsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**photos** | **int** | Total number of photos | 
**usage** | **int** | Total storage usage in bytes | 
**usage_by_user** | [**List[UsageByUserDto]**](UsageByUserDto.md) | Array of usage for each user | 
**usage_photos** | **int** | Storage usage for photos in bytes | 
**usage_videos** | **int** | Storage usage for videos in bytes | 
**videos** | **int** | Total number of videos | 

## Example

```python
from immich_sdk.models.server_stats_response_dto import ServerStatsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ServerStatsResponseDto from a JSON string
server_stats_response_dto_instance = ServerStatsResponseDto.from_json(json)
# print the JSON string representation of the object
print(ServerStatsResponseDto.to_json())

# convert the object into a dict
server_stats_response_dto_dict = server_stats_response_dto_instance.to_dict()
# create an instance of ServerStatsResponseDto from a dict
server_stats_response_dto_from_dict = ServerStatsResponseDto.from_dict(server_stats_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



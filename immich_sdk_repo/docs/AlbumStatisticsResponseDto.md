# AlbumStatisticsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**not_shared** | **int** | Number of non-shared albums | 
**owned** | **int** | Number of owned albums | 
**shared** | **int** | Number of shared albums | 

## Example

```python
from immich_sdk.models.album_statistics_response_dto import AlbumStatisticsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AlbumStatisticsResponseDto from a JSON string
album_statistics_response_dto_instance = AlbumStatisticsResponseDto.from_json(json)
# print the JSON string representation of the object
print(AlbumStatisticsResponseDto.to_json())

# convert the object into a dict
album_statistics_response_dto_dict = album_statistics_response_dto_instance.to_dict()
# create an instance of AlbumStatisticsResponseDto from a dict
album_statistics_response_dto_from_dict = AlbumStatisticsResponseDto.from_dict(album_statistics_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



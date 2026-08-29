# AssetStatsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**images** | **int** | Number of images | 
**total** | **int** | Total number of assets | 
**videos** | **int** | Number of videos | 

## Example

```python
from immich_sdk.models.asset_stats_response_dto import AssetStatsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetStatsResponseDto from a JSON string
asset_stats_response_dto_instance = AssetStatsResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetStatsResponseDto.to_json())

# convert the object into a dict
asset_stats_response_dto_dict = asset_stats_response_dto_instance.to_dict()
# create an instance of AssetStatsResponseDto from a dict
asset_stats_response_dto_from_dict = AssetStatsResponseDto.from_dict(asset_stats_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



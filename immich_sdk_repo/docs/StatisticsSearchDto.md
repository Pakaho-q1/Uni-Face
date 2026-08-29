# StatisticsSearchDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_ids** | **List[UUID]** | Filter by album IDs | [optional] 
**city** | **str** | Filter by city name | [optional] 
**country** | **str** | Filter by country name | [optional] 
**created_after** | **datetime** | Filter by creation date (after) | [optional] 
**created_before** | **datetime** | Filter by creation date (before) | [optional] 
**description** | **str** | Filter by description text | [optional] 
**filter** | [**SearchFilter**](SearchFilter.md) |  | [optional] 
**is_encoded** | **bool** | Filter by encoded status | [optional] 
**is_favorite** | **bool** | Filter by favorite status | [optional] 
**is_motion** | **bool** | Filter by motion photo status | [optional] 
**is_not_in_album** | **bool** | Filter assets not in any album | [optional] 
**is_offline** | **bool** | Filter by offline status | [optional] 
**lens_model** | **str** | Filter by lens model | [optional] 
**library_id** | **UUID** | Library ID to filter by | [optional] 
**make** | **str** | Filter by camera make | [optional] 
**model** | **str** | Filter by camera model | [optional] 
**ocr** | **str** | Filter by OCR text content | [optional] 
**person_ids** | **List[UUID]** | Filter by person IDs | [optional] 
**rating** | **int** | Filter by rating [1-5], or null for unrated | [optional] 
**state** | **str** | Filter by state/province name | [optional] 
**tag_ids** | **List[UUID]** | Filter by tag IDs | [optional] 
**taken_after** | **datetime** | Filter by taken date (after) | [optional] 
**taken_before** | **datetime** | Filter by taken date (before) | [optional] 
**trashed_after** | **datetime** | Filter by trash date (after) | [optional] 
**trashed_before** | **datetime** | Filter by trash date (before) | [optional] 
**type** | [**AssetTypeEnum**](AssetTypeEnum.md) |  | [optional] 
**updated_after** | **datetime** | Filter by update date (after) | [optional] 
**updated_before** | **datetime** | Filter by update date (before) | [optional] 
**visibility** | [**AssetVisibility**](AssetVisibility.md) |  | [optional] 

## Example

```python
from immich_sdk.models.statistics_search_dto import StatisticsSearchDto

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticsSearchDto from a JSON string
statistics_search_dto_instance = StatisticsSearchDto.from_json(json)
# print the JSON string representation of the object
print(StatisticsSearchDto.to_json())

# convert the object into a dict
statistics_search_dto_dict = statistics_search_dto_instance.to_dict()
# create an instance of StatisticsSearchDto from a dict
statistics_search_dto_from_dict = StatisticsSearchDto.from_dict(statistics_search_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



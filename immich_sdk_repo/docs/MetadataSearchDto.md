# MetadataSearchDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_ids** | **List[UUID]** | Filter by album IDs | [optional] 
**checksum** | **str** | Filter by file checksum | [optional] 
**city** | **str** | Filter by city name | [optional] 
**country** | **str** | Filter by country name | [optional] 
**created_after** | **datetime** | Filter by creation date (after) | [optional] 
**created_before** | **datetime** | Filter by creation date (before) | [optional] 
**cursor** | **str** | Cursor for the next page of results | [optional] 
**description** | **str** | Filter by description text | [optional] 
**encoded_video_path** | **str** | Filter by encoded video file path | [optional] 
**filter** | [**SearchFilter**](SearchFilter.md) |  | [optional] 
**id** | **UUID** | Filter by asset ID | [optional] 
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
**order** | [**AssetOrder**](AssetOrder.md) |  | [optional] 
**order_by** | [**SearchOrder**](SearchOrder.md) |  | [optional] 
**original_file_name** | **str** | Filter by original file name | [optional] 
**original_path** | **str** | Filter by original file path | [optional] 
**page** | **int** | Page number | [optional] 
**person_ids** | **List[UUID]** | Filter by person IDs | [optional] 
**preview_path** | **str** | Filter by preview file path | [optional] 
**rating** | **int** | Filter by rating [1-5], or null for unrated | [optional] 
**size** | **int** | Number of results to return | [optional] [default to 250]
**state** | **str** | Filter by state/province name | [optional] 
**tag_ids** | **List[UUID]** | Filter by tag IDs | [optional] 
**taken_after** | **datetime** | Filter by taken date (after) | [optional] 
**taken_before** | **datetime** | Filter by taken date (before) | [optional] 
**thumbnail_path** | **str** | Filter by thumbnail file path | [optional] 
**trashed_after** | **datetime** | Filter by trash date (after) | [optional] 
**trashed_before** | **datetime** | Filter by trash date (before) | [optional] 
**type** | [**AssetTypeEnum**](AssetTypeEnum.md) |  | [optional] 
**updated_after** | **datetime** | Filter by update date (after) | [optional] 
**updated_before** | **datetime** | Filter by update date (before) | [optional] 
**visibility** | [**AssetVisibility**](AssetVisibility.md) |  | [optional] 
**with_deleted** | **bool** | Include deleted assets | [optional] 
**with_exif** | **bool** | Include EXIF data in response | [optional] 
**with_people** | **bool** | Include people data in response | [optional] 
**with_stacked** | **bool** | Include stacked assets | [optional] 

## Example

```python
from immich_sdk.models.metadata_search_dto import MetadataSearchDto

# TODO update the JSON string below
json = "{}"
# create an instance of MetadataSearchDto from a JSON string
metadata_search_dto_instance = MetadataSearchDto.from_json(json)
# print the JSON string representation of the object
print(MetadataSearchDto.to_json())

# convert the object into a dict
metadata_search_dto_dict = metadata_search_dto_instance.to_dict()
# create an instance of MetadataSearchDto from a dict
metadata_search_dto_from_dict = MetadataSearchDto.from_dict(metadata_search_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



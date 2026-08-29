# SearchFilterBranch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_ids** | [**IdsFilter**](IdsFilter.md) |  | [optional] 
**checksum** | [**StringFilter**](StringFilter.md) |  | [optional] 
**city** | [**StringFilterNullable**](StringFilterNullable.md) |  | [optional] 
**country** | [**StringFilterNullable**](StringFilterNullable.md) |  | [optional] 
**created_at** | [**DateFilter**](DateFilter.md) |  | [optional] 
**description** | [**StringPatternFilter**](StringPatternFilter.md) |  | [optional] 
**encoded_video_path** | [**StringFilter**](StringFilter.md) |  | [optional] 
**file_size_in_bytes** | [**NumberFilter**](NumberFilter.md) |  | [optional] 
**has_albums** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**has_people** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**has_tags** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**id** | [**IdFilter**](IdFilter.md) |  | [optional] 
**is_encoded** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**is_favorite** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**is_motion** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**is_offline** | [**BoolFilter**](BoolFilter.md) |  | [optional] 
**lens_model** | [**StringFilterNullable**](StringFilterNullable.md) |  | [optional] 
**library_id** | [**IdFilterNullable**](IdFilterNullable.md) |  | [optional] 
**make** | [**StringFilterNullable**](StringFilterNullable.md) |  | [optional] 
**model** | [**StringFilterNullable**](StringFilterNullable.md) |  | [optional] 
**ocr** | [**StringSimilarityFilter**](StringSimilarityFilter.md) |  | [optional] 
**original_file_name** | [**StringPatternFilter**](StringPatternFilter.md) |  | [optional] 
**original_path** | [**StringPatternFilter**](StringPatternFilter.md) |  | [optional] 
**person_ids** | [**IdsFilter**](IdsFilter.md) |  | [optional] 
**rating** | [**NumberFilterNullable**](NumberFilterNullable.md) |  | [optional] 
**state** | [**StringFilterNullable**](StringFilterNullable.md) |  | [optional] 
**tag_ids** | [**IdsFilter**](IdsFilter.md) |  | [optional] 
**taken_at** | [**DateFilter**](DateFilter.md) |  | [optional] 
**trashed_at** | [**DateFilterNullable**](DateFilterNullable.md) |  | [optional] 
**type** | [**EnumFilterAssetType**](EnumFilterAssetType.md) |  | [optional] 
**updated_at** | [**DateFilter**](DateFilter.md) |  | [optional] 
**visibility** | [**EnumFilterAssetVisibility**](EnumFilterAssetVisibility.md) |  | [optional] 

## Example

```python
from immich_sdk.models.search_filter_branch import SearchFilterBranch

# TODO update the JSON string below
json = "{}"
# create an instance of SearchFilterBranch from a JSON string
search_filter_branch_instance = SearchFilterBranch.from_json(json)
# print the JSON string representation of the object
print(SearchFilterBranch.to_json())

# convert the object into a dict
search_filter_branch_dict = search_filter_branch_instance.to_dict()
# create an instance of SearchFilterBranch from a dict
search_filter_branch_from_dict = SearchFilterBranch.from_dict(search_filter_branch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



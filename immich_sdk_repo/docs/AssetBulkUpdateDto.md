# AssetBulkUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_time_original** | **str** | Original date and time | [optional] 
**date_time_relative** | **int** | Relative time offset in minutes | [optional] 
**description** | **str** | Asset description | [optional] 
**duplicate_id** | **str** | Duplicate ID | [optional] 
**ids** | **List[UUID]** | Asset IDs to update | 
**is_favorite** | **bool** | Mark as favorite | [optional] 
**latitude** | **float** | Latitude coordinate | [optional] 
**longitude** | **float** | Longitude coordinate | [optional] 
**rating** | **int** | Rating in range [1-5] (starred), -1 (rejected), or null (unrated) | [optional] 
**time_zone** | **str** | Time zone (IANA timezone) | [optional] 
**visibility** | [**AssetVisibility**](AssetVisibility.md) |  | [optional] 

## Example

```python
from immich_sdk.models.asset_bulk_update_dto import AssetBulkUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetBulkUpdateDto from a JSON string
asset_bulk_update_dto_instance = AssetBulkUpdateDto.from_json(json)
# print the JSON string representation of the object
print(AssetBulkUpdateDto.to_json())

# convert the object into a dict
asset_bulk_update_dto_dict = asset_bulk_update_dto_instance.to_dict()
# create an instance of AssetBulkUpdateDto from a dict
asset_bulk_update_dto_from_dict = AssetBulkUpdateDto.from_dict(asset_bulk_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



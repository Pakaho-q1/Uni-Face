# AssetBulkUploadCheckResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | [**AssetUploadAction**](AssetUploadAction.md) |  | 
**asset_id** | **UUID** | Existing asset ID if duplicate | [optional] 
**id** | **str** | Client-side identifier echoed from the request to match results to inputs | 
**is_trashed** | **bool** | Whether existing asset is trashed | [optional] 
**reason** | [**AssetRejectReason**](AssetRejectReason.md) |  | [optional] 

## Example

```python
from immich_sdk.models.asset_bulk_upload_check_result import AssetBulkUploadCheckResult

# TODO update the JSON string below
json = "{}"
# create an instance of AssetBulkUploadCheckResult from a JSON string
asset_bulk_upload_check_result_instance = AssetBulkUploadCheckResult.from_json(json)
# print the JSON string representation of the object
print(AssetBulkUploadCheckResult.to_json())

# convert the object into a dict
asset_bulk_upload_check_result_dict = asset_bulk_upload_check_result_instance.to_dict()
# create an instance of AssetBulkUploadCheckResult from a dict
asset_bulk_upload_check_result_from_dict = AssetBulkUploadCheckResult.from_dict(asset_bulk_upload_check_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



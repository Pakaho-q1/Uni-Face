# SyncAssetExifV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID | 
**city** | **str** | City | 
**country** | **str** | Country | 
**date_time_original** | **datetime** | Date time original | 
**description** | **str** | Description | 
**exif_image_height** | **int** | Exif image height | 
**exif_image_width** | **int** | Exif image width | 
**exposure_time** | **str** | Exposure time | 
**f_number** | **float** | F number | 
**file_size_in_byte** | **int** | File size in byte | 
**focal_length** | **float** | Focal length | 
**fps** | **float** | FPS | 
**iso** | **int** | ISO | 
**latitude** | **float** | Latitude | 
**lens_model** | **str** | Lens model | 
**longitude** | **float** | Longitude | 
**make** | **str** | Make | 
**model** | **str** | Model | 
**modify_date** | **datetime** | Modify date | 
**orientation** | **str** | Orientation | 
**profile_description** | **str** | Profile description | 
**projection_type** | **str** | Projection type | 
**rating** | **int** | Rating | 
**state** | **str** | State | 
**time_zone** | **str** | Time zone | 

## Example

```python
from immich_sdk.models.sync_asset_exif_v1 import SyncAssetExifV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAssetExifV1 from a JSON string
sync_asset_exif_v1_instance = SyncAssetExifV1.from_json(json)
# print the JSON string representation of the object
print(SyncAssetExifV1.to_json())

# convert the object into a dict
sync_asset_exif_v1_dict = sync_asset_exif_v1_instance.to_dict()
# create an instance of SyncAssetExifV1 from a dict
sync_asset_exif_v1_from_dict = SyncAssetExifV1.from_dict(sync_asset_exif_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



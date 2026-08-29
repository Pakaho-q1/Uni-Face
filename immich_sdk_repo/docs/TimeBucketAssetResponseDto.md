# TimeBucketAssetResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**city** | **List[Optional[str]]** | Array of city names extracted from EXIF GPS data | [optional] 
**country** | **List[Optional[str]]** | Array of country names extracted from EXIF GPS data | [optional] 
**created_at** | **List[str]** | Array of UTC timestamps when each asset was originally uploaded to Immich | 
**duration** | **List[Optional[int]]** | Array of video/gif durations in milliseconds (null for static images) | 
**file_created_at** | **List[str]** | Array of file creation timestamps in UTC | 
**id** | **List[str]** | Array of asset IDs in the time bucket | 
**is_favorite** | **List[bool]** | Array indicating whether each asset is favorited | 
**is_image** | **List[bool]** | Array indicating whether each asset is an image (false for videos) | 
**is_trashed** | **List[bool]** | Array indicating whether each asset is in the trash | 
**latitude** | **List[Optional[float]]** | Array of latitude coordinates extracted from EXIF GPS data | [optional] 
**live_photo_video_id** | **List[Optional[str]]** | Array of live photo video asset IDs (null for non-live photos) | 
**local_offset_hours** | **List[float]** | Array of UTC offset hours at the time each photo was taken. Positive values are east of UTC, negative values are west of UTC. Values may be fractional (e.g., 5.5 for +05:30, -9.75 for -09:45). Applying this offset to &#39;fileCreatedAt&#39; will give you the time the photo was taken from the photographer&#39;s perspective. | 
**longitude** | **List[Optional[float]]** | Array of longitude coordinates extracted from EXIF GPS data | [optional] 
**owner_id** | **List[str]** | Array of owner IDs for each asset | 
**projection_type** | **List[Optional[str]]** | Array of projection types for 360° content (e.g., \&quot;EQUIRECTANGULAR\&quot;, \&quot;CUBEFACE\&quot;, \&quot;CYLINDRICAL\&quot;) | 
**ratio** | **List[float]** | Array of aspect ratios (width/height) for each asset | 
**stack** | **List[Optional[List[str]]]** | Array of stack information as [stackId, assetCount] tuples (null for non-stacked assets) | [optional] 
**thumbhash** | **List[Optional[str]]** | Array of BlurHash strings for generating asset previews (base64 encoded) | 
**visibility** | [**List[AssetVisibility]**](AssetVisibility.md) | Array of visibility statuses for each asset (e.g., ARCHIVE, TIMELINE, HIDDEN, LOCKED) | 

## Example

```python
from immich_sdk.models.time_bucket_asset_response_dto import TimeBucketAssetResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of TimeBucketAssetResponseDto from a JSON string
time_bucket_asset_response_dto_instance = TimeBucketAssetResponseDto.from_json(json)
# print the JSON string representation of the object
print(TimeBucketAssetResponseDto.to_json())

# convert the object into a dict
time_bucket_asset_response_dto_dict = time_bucket_asset_response_dto_instance.to_dict()
# create an instance of TimeBucketAssetResponseDto from a dict
time_bucket_asset_response_dto_from_dict = TimeBucketAssetResponseDto.from_dict(time_bucket_asset_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



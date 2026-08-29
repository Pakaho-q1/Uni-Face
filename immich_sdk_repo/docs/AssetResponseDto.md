# AssetResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum** | **str** | Base64 encoded SHA1 hash | 
**created_at** | **datetime** | The UTC timestamp when the asset was originally uploaded to Immich. | 
**duplicate_id** | **UUID** | Duplicate group ID | [optional] 
**duration** | **int** | Video/gif duration in milliseconds (null for static images) | 
**exif_info** | [**ExifResponseDto**](ExifResponseDto.md) |  | [optional] 
**file_created_at** | **datetime** | The actual UTC timestamp when the file was created/captured, preserving timezone information. This is the authoritative timestamp for chronological sorting within timeline groups. Combined with timezone data, this can be used to determine the exact moment the photo was taken. | 
**file_modified_at** | **datetime** | The UTC timestamp when the file was last modified on the filesystem. This reflects the last time the physical file was changed, which may be different from when the photo was originally taken. | 
**has_metadata** | **bool** | Whether asset has metadata | 
**height** | **int** | Asset height | 
**id** | **UUID** | Asset ID | 
**is_archived** | **bool** | Is archived | 
**is_edited** | **bool** | Is edited | 
**is_favorite** | **bool** | Is favorite | 
**is_offline** | **bool** | Is offline | 
**is_trashed** | **bool** | Is trashed | 
**library_id** | **UUID** | Library ID | [optional] 
**live_photo_video_id** | **str** | Live photo video ID | [optional] 
**local_date_time** | **datetime** | The local date and time when the photo/video was taken, derived from EXIF metadata. This represents the photographer&#39;s local time regardless of timezone, stored as a timezone-agnostic timestamp. Used for timeline grouping by \&quot;local\&quot; days and months. | 
**original_file_name** | **str** | Original file name | 
**original_mime_type** | **str** | Original MIME type | [optional] 
**original_path** | **str** | Original file path | 
**owner** | [**UserResponseDto**](UserResponseDto.md) |  | [optional] 
**owner_id** | **UUID** | Owner user ID | 
**people** | [**List[PersonResponseDto]**](PersonResponseDto.md) |  | [optional] 
**resized** | **bool** | Is resized | [optional] 
**stack** | [**AssetStackResponseDto**](AssetStackResponseDto.md) |  | [optional] 
**tags** | [**List[TagResponseDto]**](TagResponseDto.md) |  | [optional] 
**thumbhash** | **str** | Thumbhash for thumbnail generation (base64) also used as the c query param for thumbnail cache busting. | 
**type** | [**AssetTypeEnum**](AssetTypeEnum.md) |  | 
**updated_at** | **datetime** | The UTC timestamp when the asset record was last updated in the database. This is automatically maintained by the database and reflects when any field in the asset was last modified. | 
**visibility** | [**AssetVisibility**](AssetVisibility.md) |  | 
**width** | **int** | Asset width | 

## Example

```python
from immich_sdk.models.asset_response_dto import AssetResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetResponseDto from a JSON string
asset_response_dto_instance = AssetResponseDto.from_json(json)
# print the JSON string representation of the object
print(AssetResponseDto.to_json())

# convert the object into a dict
asset_response_dto_dict = asset_response_dto_instance.to_dict()
# create an instance of AssetResponseDto from a dict
asset_response_dto_from_dict = AssetResponseDto.from_dict(asset_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



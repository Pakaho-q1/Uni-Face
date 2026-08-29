# ExifResponseDto

EXIF response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**city** | **str** | City name | [optional] 
**country** | **str** | Country name | [optional] 
**date_time_original** | **datetime** | Original date/time | [optional] 
**description** | **str** | Image description | [optional] 
**exif_image_height** | **int** | Image height in pixels | [optional] 
**exif_image_width** | **int** | Image width in pixels | [optional] 
**exposure_time** | **str** | Exposure time | [optional] 
**f_number** | **float** | F-number (aperture) | [optional] 
**file_size_in_byte** | **int** | File size in bytes | [optional] 
**focal_length** | **float** | Focal length in mm | [optional] 
**iso** | **int** | ISO sensitivity | [optional] 
**latitude** | **float** | GPS latitude | [optional] 
**lens_model** | **str** | Lens model | [optional] 
**longitude** | **float** | GPS longitude | [optional] 
**make** | **str** | Camera make | [optional] 
**model** | **str** | Camera model | [optional] 
**modify_date** | **datetime** | Modification date/time | [optional] 
**orientation** | **str** | Image orientation | [optional] 
**projection_type** | **str** | Projection type | [optional] 
**rating** | **int** | Rating | [optional] 
**state** | **str** | State/province name | [optional] 
**time_zone** | **str** | Time zone | [optional] 

## Example

```python
from immich_sdk.models.exif_response_dto import ExifResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ExifResponseDto from a JSON string
exif_response_dto_instance = ExifResponseDto.from_json(json)
# print the JSON string representation of the object
print(ExifResponseDto.to_json())

# convert the object into a dict
exif_response_dto_dict = exif_response_dto_instance.to_dict()
# create an instance of ExifResponseDto from a dict
exif_response_dto_from_dict = ExifResponseDto.from_dict(exif_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



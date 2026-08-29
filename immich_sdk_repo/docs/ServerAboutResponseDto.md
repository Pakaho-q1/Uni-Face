# ServerAboutResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**build** | **str** | Build identifier | [optional] 
**build_image** | **str** | Build image name | [optional] 
**build_image_url** | **str** | Build image URL | [optional] 
**build_url** | **str** | Build URL | [optional] 
**exiftool** | **str** | ExifTool version | [optional] 
**ffmpeg** | **str** | FFmpeg version | [optional] 
**imagemagick** | **str** | ImageMagick version | [optional] 
**libvips** | **str** | libvips version | [optional] 
**licensed** | **bool** | Whether the server is licensed | 
**nodejs** | **str** | Node.js version | [optional] 
**repository** | **str** | Repository name | [optional] 
**repository_url** | **str** | Repository URL | [optional] 
**source_commit** | **str** | Source commit hash | [optional] 
**source_ref** | **str** | Source reference (branch/tag) | [optional] 
**source_url** | **str** | Source URL | [optional] 
**third_party_bug_feature_url** | **str** | Third-party bug/feature URL | [optional] 
**third_party_documentation_url** | **str** | Third-party documentation URL | [optional] 
**third_party_source_url** | **str** | Third-party source URL | [optional] 
**third_party_support_url** | **str** | Third-party support URL | [optional] 
**version** | **str** | Server version | 
**version_url** | **str** | URL to version information | 

## Example

```python
from immich_sdk.models.server_about_response_dto import ServerAboutResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ServerAboutResponseDto from a JSON string
server_about_response_dto_instance = ServerAboutResponseDto.from_json(json)
# print the JSON string representation of the object
print(ServerAboutResponseDto.to_json())

# convert the object into a dict
server_about_response_dto_dict = server_about_response_dto_instance.to_dict()
# create an instance of ServerAboutResponseDto from a dict
server_about_response_dto_from_dict = ServerAboutResponseDto.from_dict(server_about_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



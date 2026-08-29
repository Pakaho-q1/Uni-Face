# ServerFeaturesDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config_file** | **bool** | Whether config file is available | 
**duplicate_detection** | **bool** | Whether duplicate detection is enabled | 
**email** | **bool** | Whether email notifications are enabled | 
**facial_recognition** | **bool** | Whether facial recognition is enabled | 
**import_faces** | **bool** | Whether face import is enabled | 
**map** | **bool** | Whether map feature is enabled | 
**oauth** | **bool** | Whether OAuth is enabled | 
**oauth_auto_launch** | **bool** | Whether OAuth auto-launch is enabled | 
**ocr** | **bool** | Whether OCR is enabled | 
**password_login** | **bool** | Whether password login is enabled | 
**realtime_transcoding** | **bool** | Whether real-time transcoding is enabled | 
**reverse_geocoding** | **bool** | Whether reverse geocoding is enabled | 
**search** | **bool** | Whether search is enabled | 
**sidecar** | **bool** | Whether sidecar files are supported | 
**smart_search** | **bool** | Whether smart search is enabled | 
**trash** | **bool** | Whether trash feature is enabled | 

## Example

```python
from immich_sdk.models.server_features_dto import ServerFeaturesDto

# TODO update the JSON string below
json = "{}"
# create an instance of ServerFeaturesDto from a JSON string
server_features_dto_instance = ServerFeaturesDto.from_json(json)
# print the JSON string representation of the object
print(ServerFeaturesDto.to_json())

# convert the object into a dict
server_features_dto_dict = server_features_dto_instance.to_dict()
# create an instance of ServerFeaturesDto from a dict
server_features_dto_from_dict = ServerFeaturesDto.from_dict(server_features_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



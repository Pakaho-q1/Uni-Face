# ServerApkLinksDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arm64v8a** | **str** | APK download link for ARM64 v8a architecture | 
**armeabiv7a** | **str** | APK download link for ARM EABI v7a architecture | 
**universal** | **str** | APK download link for universal architecture | 
**x86_64** | **str** | APK download link for x86_64 architecture | 

## Example

```python
from immich_sdk.models.server_apk_links_dto import ServerApkLinksDto

# TODO update the JSON string below
json = "{}"
# create an instance of ServerApkLinksDto from a JSON string
server_apk_links_dto_instance = ServerApkLinksDto.from_json(json)
# print the JSON string representation of the object
print(ServerApkLinksDto.to_json())

# convert the object into a dict
server_apk_links_dto_dict = server_apk_links_dto_instance.to_dict()
# create an instance of ServerApkLinksDto from a dict
server_apk_links_dto_from_dict = ServerApkLinksDto.from_dict(server_apk_links_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



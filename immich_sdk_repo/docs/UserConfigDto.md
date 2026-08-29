# UserConfigDto

Configuration properties that are visible to a logged user

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ffmpeg** | [**UserConfigFFmpegDto**](UserConfigFFmpegDto.md) |  | 
**image** | [**UserConfigImageDto**](UserConfigImageDto.md) |  | 
**machine_learning** | [**UserConfigMachineLearningDto**](UserConfigMachineLearningDto.md) |  | 
**map** | [**UserConfigMapDto**](UserConfigMapDto.md) |  | 
**oauth** | [**UserConfigOAuthDto**](UserConfigOAuthDto.md) |  | 
**password_login** | [**UserConfigPasswordLoginDto**](UserConfigPasswordLoginDto.md) |  | 
**reverse_geocoding** | [**UserConfigReverseGeocodingDto**](UserConfigReverseGeocodingDto.md) |  | 
**server** | [**UserConfigServerDto**](UserConfigServerDto.md) |  | 
**theme** | [**UserConfigThemeDto**](UserConfigThemeDto.md) |  | 
**trash** | [**UserConfigTrashDto**](UserConfigTrashDto.md) |  | 
**user** | [**UserConfigUserDto**](UserConfigUserDto.md) |  | 

## Example

```python
from immich_sdk.models.user_config_dto import UserConfigDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigDto from a JSON string
user_config_dto_instance = UserConfigDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigDto.to_json())

# convert the object into a dict
user_config_dto_dict = user_config_dto_instance.to_dict()
# create an instance of UserConfigDto from a dict
user_config_dto_from_dict = UserConfigDto.from_dict(user_config_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



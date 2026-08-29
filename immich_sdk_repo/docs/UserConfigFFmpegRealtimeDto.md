# UserConfigFFmpegRealtimeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enable real-time HLS transcoding (alpha) | 
**resolutions** | [**List[HlsVideoResolution]**](HlsVideoResolution.md) | Resolutions to use for real-time HLS transcoding | 
**video_codecs** | [**List[VideoCodec]**](VideoCodec.md) | Video codecs to use for real-time HLS transcoding | 

## Example

```python
from immich_sdk.models.user_config_f_fmpeg_realtime_dto import UserConfigFFmpegRealtimeDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigFFmpegRealtimeDto from a JSON string
user_config_f_fmpeg_realtime_dto_instance = UserConfigFFmpegRealtimeDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigFFmpegRealtimeDto.to_json())

# convert the object into a dict
user_config_f_fmpeg_realtime_dto_dict = user_config_f_fmpeg_realtime_dto_instance.to_dict()
# create an instance of UserConfigFFmpegRealtimeDto from a dict
user_config_f_fmpeg_realtime_dto_from_dict = UserConfigFFmpegRealtimeDto.from_dict(user_config_f_fmpeg_realtime_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AdminConfigFFmpegRealtimeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enable real-time HLS transcoding (alpha) | 
**resolutions** | [**List[HlsVideoResolution]**](HlsVideoResolution.md) | Resolutions to use for real-time HLS transcoding | 
**video_codecs** | [**List[VideoCodec]**](VideoCodec.md) | Video codecs to use for real-time HLS transcoding | 

## Example

```python
from immich_sdk.models.admin_config_f_fmpeg_realtime_dto import AdminConfigFFmpegRealtimeDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigFFmpegRealtimeDto from a JSON string
admin_config_f_fmpeg_realtime_dto_instance = AdminConfigFFmpegRealtimeDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigFFmpegRealtimeDto.to_json())

# convert the object into a dict
admin_config_f_fmpeg_realtime_dto_dict = admin_config_f_fmpeg_realtime_dto_instance.to_dict()
# create an instance of AdminConfigFFmpegRealtimeDto from a dict
admin_config_f_fmpeg_realtime_dto_from_dict = AdminConfigFFmpegRealtimeDto.from_dict(admin_config_f_fmpeg_realtime_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



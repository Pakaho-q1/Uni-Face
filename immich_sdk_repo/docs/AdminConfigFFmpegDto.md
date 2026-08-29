# AdminConfigFFmpegDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accel** | [**TranscodeHWAccel**](TranscodeHWAccel.md) |  | 
**accel_decode** | **bool** | Accelerated decode | 
**accepted_audio_codecs** | [**List[AudioCodec]**](AudioCodec.md) | Accepted audio codecs | 
**accepted_containers** | [**List[VideoContainer]**](VideoContainer.md) | Accepted containers | 
**accepted_video_codecs** | [**List[VideoCodec]**](VideoCodec.md) | Accepted video codecs | 
**bframes** | **int** | B-frames | 
**cq_mode** | [**CQMode**](CQMode.md) |  | 
**crf** | **int** | CRF | 
**gop_size** | **int** | GOP size | 
**max_bitrate** | **str** | Max bitrate | 
**preferred_hw_device** | **str** | Preferred hardware device | 
**preset** | **str** | Preset | 
**realtime** | [**AdminConfigFFmpegRealtimeDto**](AdminConfigFFmpegRealtimeDto.md) |  | 
**refs** | **int** | References | 
**target_audio_codec** | [**AudioCodec**](AudioCodec.md) |  | 
**target_resolution** | **str** | Target resolution | 
**target_video_codec** | [**VideoCodec**](VideoCodec.md) |  | 
**temporal_aq** | **bool** | Temporal AQ | 
**threads** | **int** | Threads | 
**tonemap** | [**ToneMapping**](ToneMapping.md) |  | 
**transcode** | [**TranscodePolicy**](TranscodePolicy.md) |  | 
**two_pass** | **bool** | Two pass | 

## Example

```python
from immich_sdk.models.admin_config_f_fmpeg_dto import AdminConfigFFmpegDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigFFmpegDto from a JSON string
admin_config_f_fmpeg_dto_instance = AdminConfigFFmpegDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigFFmpegDto.to_json())

# convert the object into a dict
admin_config_f_fmpeg_dto_dict = admin_config_f_fmpeg_dto_instance.to_dict()
# create an instance of AdminConfigFFmpegDto from a dict
admin_config_f_fmpeg_dto_from_dict = AdminConfigFFmpegDto.from_dict(admin_config_f_fmpeg_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



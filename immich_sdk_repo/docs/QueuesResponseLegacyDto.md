# QueuesResponseLegacyDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**background_task** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**backup_database** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**duplicate_detection** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**editor** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**face_detection** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**facial_recognition** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**integrity_check** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**library** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**metadata_extraction** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**migration** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**notifications** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**ocr** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**search** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**sidecar** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**smart_search** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**storage_template_migration** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**thumbnail_generation** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**video_conversion** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 
**workflow** | [**QueueResponseLegacyDto**](QueueResponseLegacyDto.md) |  | 

## Example

```python
from immich_sdk.models.queues_response_legacy_dto import QueuesResponseLegacyDto

# TODO update the JSON string below
json = "{}"
# create an instance of QueuesResponseLegacyDto from a JSON string
queues_response_legacy_dto_instance = QueuesResponseLegacyDto.from_json(json)
# print the JSON string representation of the object
print(QueuesResponseLegacyDto.to_json())

# convert the object into a dict
queues_response_legacy_dto_dict = queues_response_legacy_dto_instance.to_dict()
# create an instance of QueuesResponseLegacyDto from a dict
queues_response_legacy_dto_from_dict = QueuesResponseLegacyDto.from_dict(queues_response_legacy_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



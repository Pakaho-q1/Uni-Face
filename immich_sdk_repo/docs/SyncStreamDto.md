# SyncStreamDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reset** | **bool** | Reset sync state | [optional] 
**types** | [**List[SyncRequestType]**](SyncRequestType.md) | Sync request types | 

## Example

```python
from immich_sdk.models.sync_stream_dto import SyncStreamDto

# TODO update the JSON string below
json = "{}"
# create an instance of SyncStreamDto from a JSON string
sync_stream_dto_instance = SyncStreamDto.from_json(json)
# print the JSON string representation of the object
print(SyncStreamDto.to_json())

# convert the object into a dict
sync_stream_dto_dict = sync_stream_dto_instance.to_dict()
# create an instance of SyncStreamDto from a dict
sync_stream_dto_from_dict = SyncStreamDto.from_dict(sync_stream_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



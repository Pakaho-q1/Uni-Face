# SyncAckSetDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**acks** | **List[str]** | Acknowledgment IDs (max 1000) | 

## Example

```python
from immich_sdk.models.sync_ack_set_dto import SyncAckSetDto

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAckSetDto from a JSON string
sync_ack_set_dto_instance = SyncAckSetDto.from_json(json)
# print the JSON string representation of the object
print(SyncAckSetDto.to_json())

# convert the object into a dict
sync_ack_set_dto_dict = sync_ack_set_dto_instance.to_dict()
# create an instance of SyncAckSetDto from a dict
sync_ack_set_dto_from_dict = SyncAckSetDto.from_dict(sync_ack_set_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



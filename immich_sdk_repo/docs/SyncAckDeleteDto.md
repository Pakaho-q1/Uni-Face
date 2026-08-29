# SyncAckDeleteDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**types** | [**List[SyncEntityType]**](SyncEntityType.md) | Sync entity types to delete acks for | [optional] 

## Example

```python
from immich_sdk.models.sync_ack_delete_dto import SyncAckDeleteDto

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAckDeleteDto from a JSON string
sync_ack_delete_dto_instance = SyncAckDeleteDto.from_json(json)
# print the JSON string representation of the object
print(SyncAckDeleteDto.to_json())

# convert the object into a dict
sync_ack_delete_dto_dict = sync_ack_delete_dto_instance.to_dict()
# create an instance of SyncAckDeleteDto from a dict
sync_ack_delete_dto_from_dict = SyncAckDeleteDto.from_dict(sync_ack_delete_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



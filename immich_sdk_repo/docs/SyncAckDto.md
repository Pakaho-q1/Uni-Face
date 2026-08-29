# SyncAckDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ack** | **str** | Acknowledgment ID | 
**type** | [**SyncEntityType**](SyncEntityType.md) |  | 

## Example

```python
from immich_sdk.models.sync_ack_dto import SyncAckDto

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAckDto from a JSON string
sync_ack_dto_instance = SyncAckDto.from_json(json)
# print the JSON string representation of the object
print(SyncAckDto.to_json())

# convert the object into a dict
sync_ack_dto_dict = sync_ack_dto_instance.to_dict()
# create an instance of SyncAckDto from a dict
sync_ack_dto_from_dict = SyncAckDto.from_dict(sync_ack_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



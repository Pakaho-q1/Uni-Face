# SyncMemoryV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Created at | 
**data** | **Dict[str, object]** | Data | 
**deleted_at** | **datetime** | Deleted at | 
**hide_at** | **datetime** | Hide at | 
**id** | **UUID** | Memory ID | 
**is_saved** | **bool** | Is saved | 
**memory_at** | **datetime** | Memory at | 
**owner_id** | **UUID** | Owner ID | 
**seen_at** | **datetime** | Seen at | 
**show_at** | **datetime** | Show at | 
**type** | [**MemoryType**](MemoryType.md) |  | 
**updated_at** | **datetime** | Updated at | 

## Example

```python
from immich_sdk.models.sync_memory_v1 import SyncMemoryV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncMemoryV1 from a JSON string
sync_memory_v1_instance = SyncMemoryV1.from_json(json)
# print the JSON string representation of the object
print(SyncMemoryV1.to_json())

# convert the object into a dict
sync_memory_v1_dict = sync_memory_v1_instance.to_dict()
# create an instance of SyncMemoryV1 from a dict
sync_memory_v1_from_dict = SyncMemoryV1.from_dict(sync_memory_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



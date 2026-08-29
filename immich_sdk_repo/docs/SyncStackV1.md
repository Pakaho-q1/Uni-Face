# SyncStackV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Created at | 
**id** | **UUID** | Stack ID | 
**owner_id** | **UUID** | Owner ID | 
**primary_asset_id** | **UUID** | Primary asset ID | 
**updated_at** | **datetime** | Updated at | 

## Example

```python
from immich_sdk.models.sync_stack_v1 import SyncStackV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncStackV1 from a JSON string
sync_stack_v1_instance = SyncStackV1.from_json(json)
# print the JSON string representation of the object
print(SyncStackV1.to_json())

# convert the object into a dict
sync_stack_v1_dict = sync_stack_v1_instance.to_dict()
# create an instance of SyncStackV1 from a dict
sync_stack_v1_from_dict = SyncStackV1.from_dict(sync_stack_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



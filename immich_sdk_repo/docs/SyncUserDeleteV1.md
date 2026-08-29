# SyncUserDeleteV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **UUID** | User ID | 

## Example

```python
from immich_sdk.models.sync_user_delete_v1 import SyncUserDeleteV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncUserDeleteV1 from a JSON string
sync_user_delete_v1_instance = SyncUserDeleteV1.from_json(json)
# print the JSON string representation of the object
print(SyncUserDeleteV1.to_json())

# convert the object into a dict
sync_user_delete_v1_dict = sync_user_delete_v1_instance.to_dict()
# create an instance of SyncUserDeleteV1 from a dict
sync_user_delete_v1_from_dict = SyncUserDeleteV1.from_dict(sync_user_delete_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



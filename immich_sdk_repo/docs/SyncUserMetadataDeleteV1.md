# SyncUserMetadataDeleteV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | [**UserMetadataKey**](UserMetadataKey.md) |  | 
**user_id** | **UUID** | User ID | 

## Example

```python
from immich_sdk.models.sync_user_metadata_delete_v1 import SyncUserMetadataDeleteV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncUserMetadataDeleteV1 from a JSON string
sync_user_metadata_delete_v1_instance = SyncUserMetadataDeleteV1.from_json(json)
# print the JSON string representation of the object
print(SyncUserMetadataDeleteV1.to_json())

# convert the object into a dict
sync_user_metadata_delete_v1_dict = sync_user_metadata_delete_v1_instance.to_dict()
# create an instance of SyncUserMetadataDeleteV1 from a dict
sync_user_metadata_delete_v1_from_dict = SyncUserMetadataDeleteV1.from_dict(sync_user_metadata_delete_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



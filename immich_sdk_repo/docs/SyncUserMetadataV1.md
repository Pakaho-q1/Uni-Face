# SyncUserMetadataV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | [**UserMetadataKey**](UserMetadataKey.md) |  | 
**user_id** | **UUID** | User ID | 
**value** | **Dict[str, object]** | User metadata value | 

## Example

```python
from immich_sdk.models.sync_user_metadata_v1 import SyncUserMetadataV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncUserMetadataV1 from a JSON string
sync_user_metadata_v1_instance = SyncUserMetadataV1.from_json(json)
# print the JSON string representation of the object
print(SyncUserMetadataV1.to_json())

# convert the object into a dict
sync_user_metadata_v1_dict = sync_user_metadata_v1_instance.to_dict()
# create an instance of SyncUserMetadataV1 from a dict
sync_user_metadata_v1_from_dict = SyncUserMetadataV1.from_dict(sync_user_metadata_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# SyncAuthUserV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avatar_color** | [**UserAvatarColor**](UserAvatarColor.md) |  | [optional] 
**deleted_at** | **datetime** | User deleted at | 
**email** | **str** | User email | 
**has_profile_image** | **bool** | User has profile image | 
**id** | **UUID** | User ID | 
**is_admin** | **bool** | User is admin | 
**name** | **str** | User name | 
**oauth_id** | **str** | User OAuth ID | 
**pin_code** | **str** | User pin code | 
**profile_changed_at** | **datetime** | User profile changed at | 
**quota_size_in_bytes** | **int** | Quota size in bytes | 
**quota_usage_in_bytes** | **int** | Quota usage in bytes | 
**storage_label** | **str** | User storage label | 

## Example

```python
from immich_sdk.models.sync_auth_user_v1 import SyncAuthUserV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncAuthUserV1 from a JSON string
sync_auth_user_v1_instance = SyncAuthUserV1.from_json(json)
# print the JSON string representation of the object
print(SyncAuthUserV1.to_json())

# convert the object into a dict
sync_auth_user_v1_dict = sync_auth_user_v1_instance.to_dict()
# create an instance of SyncAuthUserV1 from a dict
sync_auth_user_v1_from_dict = SyncAuthUserV1.from_dict(sync_auth_user_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



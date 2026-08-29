# UserAdminResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avatar_color** | [**UserAvatarColor**](UserAvatarColor.md) |  | 
**cluster_group_id** | **UUID** | Cluster group the user is a member of | 
**created_at** | **datetime** | Creation date | 
**deleted_at** | **datetime** | Deletion date | 
**email** | **str** | User email | 
**id** | **UUID** | User ID | 
**is_admin** | **bool** | Is admin user | 
**license** | [**UserLicense**](UserLicense.md) |  | 
**name** | **str** | User name | 
**oauth_id** | **str** | OAuth ID | 
**profile_changed_at** | **datetime** | Profile change date | 
**profile_image_path** | **str** | Profile image path | 
**quota_size_in_bytes** | **int** | Storage quota in bytes | 
**quota_usage_in_bytes** | **int** | Storage usage in bytes | 
**should_change_password** | **bool** | Require password change on next login | 
**status** | [**UserStatus**](UserStatus.md) |  | 
**storage_label** | **str** | Storage label | 
**updated_at** | **datetime** | Last update date | 

## Example

```python
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserAdminResponseDto from a JSON string
user_admin_response_dto_instance = UserAdminResponseDto.from_json(json)
# print the JSON string representation of the object
print(UserAdminResponseDto.to_json())

# convert the object into a dict
user_admin_response_dto_dict = user_admin_response_dto_instance.to_dict()
# create an instance of UserAdminResponseDto from a dict
user_admin_response_dto_from_dict = UserAdminResponseDto.from_dict(user_admin_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



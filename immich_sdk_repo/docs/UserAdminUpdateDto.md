# UserAdminUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avatar_color** | [**UserAvatarColor**](UserAvatarColor.md) |  | [optional] 
**email** | **str** | User email | [optional] 
**is_admin** | **bool** | Grant admin privileges | [optional] 
**name** | **str** | User name | [optional] 
**password** | **str** | User password | [optional] 
**pin_code** | **str** | PIN code | [optional] 
**quota_size_in_bytes** | **int** | Storage quota in bytes | [optional] 
**should_change_password** | **bool** | Require password change on next login | [optional] 
**storage_label** | **str** | Storage label | [optional] 

## Example

```python
from immich_sdk.models.user_admin_update_dto import UserAdminUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserAdminUpdateDto from a JSON string
user_admin_update_dto_instance = UserAdminUpdateDto.from_json(json)
# print the JSON string representation of the object
print(UserAdminUpdateDto.to_json())

# convert the object into a dict
user_admin_update_dto_dict = user_admin_update_dto_instance.to_dict()
# create an instance of UserAdminUpdateDto from a dict
user_admin_update_dto_from_dict = UserAdminUpdateDto.from_dict(user_admin_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# UserAdminCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avatar_color** | [**UserAvatarColor**](UserAvatarColor.md) |  | [optional] 
**email** | **str** | User email | 
**is_admin** | **bool** | Grant admin privileges | [optional] 
**name** | **str** | User name | 
**notify** | **bool** | Send notification email | [optional] 
**password** | **str** | User password | 
**pin_code** | **str** | PIN code | [optional] 
**quota_size_in_bytes** | **int** | Storage quota in bytes | [optional] 
**should_change_password** | **bool** | Require password change on next login | [optional] 
**storage_label** | **str** | Storage label | [optional] 

## Example

```python
from immich_sdk.models.user_admin_create_dto import UserAdminCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserAdminCreateDto from a JSON string
user_admin_create_dto_instance = UserAdminCreateDto.from_json(json)
# print the JSON string representation of the object
print(UserAdminCreateDto.to_json())

# convert the object into a dict
user_admin_create_dto_dict = user_admin_create_dto_instance.to_dict()
# create an instance of UserAdminCreateDto from a dict
user_admin_create_dto_from_dict = UserAdminCreateDto.from_dict(user_admin_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



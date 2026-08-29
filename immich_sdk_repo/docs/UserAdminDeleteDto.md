# UserAdminDeleteDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**force** | **bool** | Force delete even if user has assets | [optional] 

## Example

```python
from immich_sdk.models.user_admin_delete_dto import UserAdminDeleteDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserAdminDeleteDto from a JSON string
user_admin_delete_dto_instance = UserAdminDeleteDto.from_json(json)
# print the JSON string representation of the object
print(UserAdminDeleteDto.to_json())

# convert the object into a dict
user_admin_delete_dto_dict = user_admin_delete_dto_instance.to_dict()
# create an instance of UserAdminDeleteDto from a dict
user_admin_delete_dto_from_dict = UserAdminDeleteDto.from_dict(user_admin_delete_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



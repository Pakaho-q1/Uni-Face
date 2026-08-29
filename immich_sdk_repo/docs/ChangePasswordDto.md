# ChangePasswordDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invalidate_sessions** | **bool** | Invalidate all other sessions | [optional] [default to False]
**new_password** | **str** | New password (min 8 characters) | 
**password** | **str** | Current password | 

## Example

```python
from immich_sdk.models.change_password_dto import ChangePasswordDto

# TODO update the JSON string below
json = "{}"
# create an instance of ChangePasswordDto from a JSON string
change_password_dto_instance = ChangePasswordDto.from_json(json)
# print the JSON string representation of the object
print(ChangePasswordDto.to_json())

# convert the object into a dict
change_password_dto_dict = change_password_dto_instance.to_dict()
# create an instance of ChangePasswordDto from a dict
change_password_dto_from_dict = ChangePasswordDto.from_dict(change_password_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



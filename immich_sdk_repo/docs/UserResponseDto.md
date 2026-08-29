# UserResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avatar_color** | [**UserAvatarColor**](UserAvatarColor.md) |  | 
**email** | **str** | User email | 
**id** | **UUID** | User ID | 
**name** | **str** | User name | 
**profile_changed_at** | **datetime** | Profile change date | 
**profile_image_path** | **str** | Profile image path | 

## Example

```python
from immich_sdk.models.user_response_dto import UserResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserResponseDto from a JSON string
user_response_dto_instance = UserResponseDto.from_json(json)
# print the JSON string representation of the object
print(UserResponseDto.to_json())

# convert the object into a dict
user_response_dto_dict = user_response_dto_instance.to_dict()
# create an instance of UserResponseDto from a dict
user_response_dto_from_dict = UserResponseDto.from_dict(user_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



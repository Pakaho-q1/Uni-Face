# LoginResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_token** | **str** | Access token | 
**is_admin** | **bool** | Is admin user | 
**is_onboarded** | **bool** | Is onboarded | 
**name** | **str** | User name | 
**profile_image_path** | **str** | Profile image path | 
**should_change_password** | **bool** | Should change password | 
**user_email** | **str** | User email | 
**user_id** | **UUID** | User ID | 

## Example

```python
from immich_sdk.models.login_response_dto import LoginResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of LoginResponseDto from a JSON string
login_response_dto_instance = LoginResponseDto.from_json(json)
# print the JSON string representation of the object
print(LoginResponseDto.to_json())

# convert the object into a dict
login_response_dto_dict = login_response_dto_instance.to_dict()
# create an instance of LoginResponseDto from a dict
login_response_dto_from_dict = LoginResponseDto.from_dict(login_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



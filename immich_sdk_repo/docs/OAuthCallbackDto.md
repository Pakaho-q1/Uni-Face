# OAuthCallbackDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code_verifier** | **str** | OAuth code verifier (PKCE) | [optional] 
**state** | **str** | OAuth state parameter | [optional] 
**url** | **str** | OAuth callback URL | 

## Example

```python
from immich_sdk.models.o_auth_callback_dto import OAuthCallbackDto

# TODO update the JSON string below
json = "{}"
# create an instance of OAuthCallbackDto from a JSON string
o_auth_callback_dto_instance = OAuthCallbackDto.from_json(json)
# print the JSON string representation of the object
print(OAuthCallbackDto.to_json())

# convert the object into a dict
o_auth_callback_dto_dict = o_auth_callback_dto_instance.to_dict()
# create an instance of OAuthCallbackDto from a dict
o_auth_callback_dto_from_dict = OAuthCallbackDto.from_dict(o_auth_callback_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



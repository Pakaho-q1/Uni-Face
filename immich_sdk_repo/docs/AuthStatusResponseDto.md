# AuthStatusResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expires_at** | **str** | Session expiration date | [optional] 
**is_elevated** | **bool** | Is elevated session | 
**password** | **bool** | Has password set | 
**pin_code** | **bool** | Has PIN code set | 
**pin_expires_at** | **str** | PIN expiration date | [optional] 

## Example

```python
from immich_sdk.models.auth_status_response_dto import AuthStatusResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of AuthStatusResponseDto from a JSON string
auth_status_response_dto_instance = AuthStatusResponseDto.from_json(json)
# print the JSON string representation of the object
print(AuthStatusResponseDto.to_json())

# convert the object into a dict
auth_status_response_dto_dict = auth_status_response_dto_instance.to_dict()
# create an instance of AuthStatusResponseDto from a dict
auth_status_response_dto_from_dict = AuthStatusResponseDto.from_dict(auth_status_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



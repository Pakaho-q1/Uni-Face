# SessionCreateResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app_version** | **str** | App version | 
**created_at** | **str** | Creation date | 
**current** | **bool** | Is current session | 
**device_os** | **str** | Device OS | 
**device_type** | **str** | Device type | 
**expires_at** | **str** | Expiration date | [optional] 
**id** | **UUID** | Session ID | 
**is_pending_sync_reset** | **bool** | Is pending sync reset | 
**token** | **str** | Session token | 
**updated_at** | **str** | Last update date | 

## Example

```python
from immich_sdk.models.session_create_response_dto import SessionCreateResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of SessionCreateResponseDto from a JSON string
session_create_response_dto_instance = SessionCreateResponseDto.from_json(json)
# print the JSON string representation of the object
print(SessionCreateResponseDto.to_json())

# convert the object into a dict
session_create_response_dto_dict = session_create_response_dto_instance.to_dict()
# create an instance of SessionCreateResponseDto from a dict
session_create_response_dto_from_dict = SessionCreateResponseDto.from_dict(session_create_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



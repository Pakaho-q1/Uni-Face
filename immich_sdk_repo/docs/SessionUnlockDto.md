# SessionUnlockDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**password** | **str** | User password (required if PIN code is not provided) | [optional] 
**pin_code** | **str** | New PIN code (4-6 digits) | [optional] 

## Example

```python
from immich_sdk.models.session_unlock_dto import SessionUnlockDto

# TODO update the JSON string below
json = "{}"
# create an instance of SessionUnlockDto from a JSON string
session_unlock_dto_instance = SessionUnlockDto.from_json(json)
# print the JSON string representation of the object
print(SessionUnlockDto.to_json())

# convert the object into a dict
session_unlock_dto_dict = session_unlock_dto_instance.to_dict()
# create an instance of SessionUnlockDto from a dict
session_unlock_dto_from_dict = SessionUnlockDto.from_dict(session_unlock_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



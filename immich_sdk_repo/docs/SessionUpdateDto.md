# SessionUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_pending_sync_reset** | **bool** | Reset pending sync state | [optional] 

## Example

```python
from immich_sdk.models.session_update_dto import SessionUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of SessionUpdateDto from a JSON string
session_update_dto_instance = SessionUpdateDto.from_json(json)
# print the JSON string representation of the object
print(SessionUpdateDto.to_json())

# convert the object into a dict
session_update_dto_dict = session_update_dto_instance.to_dict()
# create an instance of SessionUpdateDto from a dict
session_update_dto_from_dict = SessionUpdateDto.from_dict(session_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



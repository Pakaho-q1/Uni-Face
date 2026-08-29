# SessionCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_os** | **str** | Device OS | [optional] 
**device_type** | **str** | Device type | [optional] 
**duration** | **int** | Session duration in seconds | [optional] 

## Example

```python
from immich_sdk.models.session_create_dto import SessionCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of SessionCreateDto from a JSON string
session_create_dto_instance = SessionCreateDto.from_json(json)
# print the JSON string representation of the object
print(SessionCreateDto.to_json())

# convert the object into a dict
session_create_dto_dict = session_create_dto_instance.to_dict()
# create an instance of SessionCreateDto from a dict
session_create_dto_from_dict = SessionCreateDto.from_dict(session_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



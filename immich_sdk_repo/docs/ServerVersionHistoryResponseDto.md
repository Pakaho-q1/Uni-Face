# ServerVersionHistoryResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | When this version was first seen | 
**id** | **UUID** | Version history entry ID | 
**version** | **str** | Version string | 

## Example

```python
from immich_sdk.models.server_version_history_response_dto import ServerVersionHistoryResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ServerVersionHistoryResponseDto from a JSON string
server_version_history_response_dto_instance = ServerVersionHistoryResponseDto.from_json(json)
# print the JSON string representation of the object
print(ServerVersionHistoryResponseDto.to_json())

# convert the object into a dict
server_version_history_response_dto_dict = server_version_history_response_dto_instance.to_dict()
# create an instance of ServerVersionHistoryResponseDto from a dict
server_version_history_response_dto_from_dict = ServerVersionHistoryResponseDto.from_dict(server_version_history_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



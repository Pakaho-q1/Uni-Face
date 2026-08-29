# ReleaseEventV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checked_at** | **str** | When the server last checked for a latest version. As an ISO timestamp | 
**is_available** | **bool** | Whether a new version is available | 
**release_version** | [**ServerVersionResponseDto**](ServerVersionResponseDto.md) |  | 
**server_version** | [**ServerVersionResponseDto**](ServerVersionResponseDto.md) |  | 
**type** | [**ReleaseType**](ReleaseType.md) |  | 

## Example

```python
from immich_sdk.models.release_event_v1 import ReleaseEventV1

# TODO update the JSON string below
json = "{}"
# create an instance of ReleaseEventV1 from a JSON string
release_event_v1_instance = ReleaseEventV1.from_json(json)
# print the JSON string representation of the object
print(ReleaseEventV1.to_json())

# convert the object into a dict
release_event_v1_dict = release_event_v1_instance.to_dict()
# create an instance of ReleaseEventV1 from a dict
release_event_v1_from_dict = ReleaseEventV1.from_dict(release_event_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



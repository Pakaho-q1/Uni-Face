# UserConfigClipDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 

## Example

```python
from immich_sdk.models.user_config_clip_dto import UserConfigClipDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigClipDto from a JSON string
user_config_clip_dto_instance = UserConfigClipDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigClipDto.to_json())

# convert the object into a dict
user_config_clip_dto_dict = user_config_clip_dto_instance.to_dict()
# create an instance of UserConfigClipDto from a dict
user_config_clip_dto_from_dict = UserConfigClipDto.from_dict(user_config_clip_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



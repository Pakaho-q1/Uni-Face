# AdminConfigClipDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 
**model_name** | **str** | Name of the model to use | 

## Example

```python
from immich_sdk.models.admin_config_clip_dto import AdminConfigClipDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigClipDto from a JSON string
admin_config_clip_dto_instance = AdminConfigClipDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigClipDto.to_json())

# convert the object into a dict
admin_config_clip_dto_dict = admin_config_clip_dto_instance.to_dict()
# create an instance of AdminConfigClipDto from a dict
admin_config_clip_dto_from_dict = AdminConfigClipDto.from_dict(admin_config_clip_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



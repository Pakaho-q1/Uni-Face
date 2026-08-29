# AdminConfigGeneratedFullsizeImageDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 
**format** | [**ImageFormat**](ImageFormat.md) |  | 
**progressive** | **bool** | Progressive | [optional] 
**quality** | **int** | Quality | 

## Example

```python
from immich_sdk.models.admin_config_generated_fullsize_image_dto import AdminConfigGeneratedFullsizeImageDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigGeneratedFullsizeImageDto from a JSON string
admin_config_generated_fullsize_image_dto_instance = AdminConfigGeneratedFullsizeImageDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigGeneratedFullsizeImageDto.to_json())

# convert the object into a dict
admin_config_generated_fullsize_image_dto_dict = admin_config_generated_fullsize_image_dto_instance.to_dict()
# create an instance of AdminConfigGeneratedFullsizeImageDto from a dict
admin_config_generated_fullsize_image_dto_from_dict = AdminConfigGeneratedFullsizeImageDto.from_dict(admin_config_generated_fullsize_image_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



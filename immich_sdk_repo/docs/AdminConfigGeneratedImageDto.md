# AdminConfigGeneratedImageDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | [**ImageFormat**](ImageFormat.md) |  | 
**progressive** | **bool** | Progressive | [optional] 
**quality** | **int** | Quality | 
**size** | **int** | Size | 

## Example

```python
from immich_sdk.models.admin_config_generated_image_dto import AdminConfigGeneratedImageDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigGeneratedImageDto from a JSON string
admin_config_generated_image_dto_instance = AdminConfigGeneratedImageDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigGeneratedImageDto.to_json())

# convert the object into a dict
admin_config_generated_image_dto_dict = admin_config_generated_image_dto_instance.to_dict()
# create an instance of AdminConfigGeneratedImageDto from a dict
admin_config_generated_image_dto_from_dict = AdminConfigGeneratedImageDto.from_dict(admin_config_generated_image_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



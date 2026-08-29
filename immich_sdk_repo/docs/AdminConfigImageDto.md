# AdminConfigImageDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**colorspace** | [**Colorspace**](Colorspace.md) |  | 
**extract_embedded** | **bool** | Extract embedded | 
**fullsize** | [**AdminConfigGeneratedFullsizeImageDto**](AdminConfigGeneratedFullsizeImageDto.md) |  | 
**preview** | [**AdminConfigGeneratedImageDto**](AdminConfigGeneratedImageDto.md) |  | 
**thumbnail** | [**AdminConfigGeneratedImageDto**](AdminConfigGeneratedImageDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_image_dto import AdminConfigImageDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigImageDto from a JSON string
admin_config_image_dto_instance = AdminConfigImageDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigImageDto.to_json())

# convert the object into a dict
admin_config_image_dto_dict = admin_config_image_dto_instance.to_dict()
# create an instance of AdminConfigImageDto from a dict
admin_config_image_dto_from_dict = AdminConfigImageDto.from_dict(admin_config_image_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



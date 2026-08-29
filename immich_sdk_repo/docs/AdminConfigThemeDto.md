# AdminConfigThemeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_css** | **str** | Custom CSS for theming | 

## Example

```python
from immich_sdk.models.admin_config_theme_dto import AdminConfigThemeDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigThemeDto from a JSON string
admin_config_theme_dto_instance = AdminConfigThemeDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigThemeDto.to_json())

# convert the object into a dict
admin_config_theme_dto_dict = admin_config_theme_dto_instance.to_dict()
# create an instance of AdminConfigThemeDto from a dict
admin_config_theme_dto_from_dict = AdminConfigThemeDto.from_dict(admin_config_theme_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



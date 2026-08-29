# UserConfigThemeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_css** | **str** | Custom CSS for theming | 

## Example

```python
from immich_sdk.models.user_config_theme_dto import UserConfigThemeDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigThemeDto from a JSON string
user_config_theme_dto_instance = UserConfigThemeDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigThemeDto.to_json())

# convert the object into a dict
user_config_theme_dto_dict = user_config_theme_dto_instance.to_dict()
# create an instance of UserConfigThemeDto from a dict
user_config_theme_dto_from_dict = UserConfigThemeDto.from_dict(user_config_theme_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



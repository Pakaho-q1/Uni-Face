# PublicConfigThemeDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_css** | **str** | Custom CSS for theming | 

## Example

```python
from immich_sdk.models.public_config_theme_dto import PublicConfigThemeDto

# TODO update the JSON string below
json = "{}"
# create an instance of PublicConfigThemeDto from a JSON string
public_config_theme_dto_instance = PublicConfigThemeDto.from_json(json)
# print the JSON string representation of the object
print(PublicConfigThemeDto.to_json())

# convert the object into a dict
public_config_theme_dto_dict = public_config_theme_dto_instance.to_dict()
# create an instance of PublicConfigThemeDto from a dict
public_config_theme_dto_from_dict = PublicConfigThemeDto.from_dict(public_config_theme_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



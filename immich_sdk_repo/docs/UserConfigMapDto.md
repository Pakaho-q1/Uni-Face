# UserConfigMapDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dark_style** | **str** | Dark map style URL | 
**enabled** | **bool** | Enabled | 
**light_style** | **str** | Light map style URL | 

## Example

```python
from immich_sdk.models.user_config_map_dto import UserConfigMapDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigMapDto from a JSON string
user_config_map_dto_instance = UserConfigMapDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigMapDto.to_json())

# convert the object into a dict
user_config_map_dto_dict = user_config_map_dto_instance.to_dict()
# create an instance of UserConfigMapDto from a dict
user_config_map_dto_from_dict = UserConfigMapDto.from_dict(user_config_map_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



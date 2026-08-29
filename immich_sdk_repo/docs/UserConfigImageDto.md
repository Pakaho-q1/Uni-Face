# UserConfigImageDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fullsize** | [**UserConfigGeneratedFullsizeImageDto**](UserConfigGeneratedFullsizeImageDto.md) |  | 
**preview** | [**UserConfigGeneratedImageDto**](UserConfigGeneratedImageDto.md) |  | 
**thumbnail** | [**UserConfigGeneratedImageDto**](UserConfigGeneratedImageDto.md) |  | 

## Example

```python
from immich_sdk.models.user_config_image_dto import UserConfigImageDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigImageDto from a JSON string
user_config_image_dto_instance = UserConfigImageDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigImageDto.to_json())

# convert the object into a dict
user_config_image_dto_dict = user_config_image_dto_instance.to_dict()
# create an instance of UserConfigImageDto from a dict
user_config_image_dto_from_dict = UserConfigImageDto.from_dict(user_config_image_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



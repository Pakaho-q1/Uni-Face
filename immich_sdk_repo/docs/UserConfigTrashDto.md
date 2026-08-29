# UserConfigTrashDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**days** | **int** | Days | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.user_config_trash_dto import UserConfigTrashDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigTrashDto from a JSON string
user_config_trash_dto_instance = UserConfigTrashDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigTrashDto.to_json())

# convert the object into a dict
user_config_trash_dto_dict = user_config_trash_dto_instance.to_dict()
# create an instance of UserConfigTrashDto from a dict
user_config_trash_dto_from_dict = UserConfigTrashDto.from_dict(user_config_trash_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



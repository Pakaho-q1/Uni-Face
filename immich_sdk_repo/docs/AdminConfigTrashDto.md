# AdminConfigTrashDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**days** | **int** | Days | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_trash_dto import AdminConfigTrashDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigTrashDto from a JSON string
admin_config_trash_dto_instance = AdminConfigTrashDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigTrashDto.to_json())

# convert the object into a dict
admin_config_trash_dto_dict = admin_config_trash_dto_instance.to_dict()
# create an instance of AdminConfigTrashDto from a dict
admin_config_trash_dto_from_dict = AdminConfigTrashDto.from_dict(admin_config_trash_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



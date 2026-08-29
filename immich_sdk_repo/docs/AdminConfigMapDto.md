# AdminConfigMapDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dark_style** | **str** | Dark map style URL | 
**enabled** | **bool** | Enabled | 
**light_style** | **str** | Light map style URL | 

## Example

```python
from immich_sdk.models.admin_config_map_dto import AdminConfigMapDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigMapDto from a JSON string
admin_config_map_dto_instance = AdminConfigMapDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigMapDto.to_json())

# convert the object into a dict
admin_config_map_dto_dict = admin_config_map_dto_instance.to_dict()
# create an instance of AdminConfigMapDto from a dict
admin_config_map_dto_from_dict = AdminConfigMapDto.from_dict(admin_config_map_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



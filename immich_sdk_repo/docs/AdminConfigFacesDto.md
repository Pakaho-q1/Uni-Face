# AdminConfigFacesDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_import** | **bool** | Import | 

## Example

```python
from immich_sdk.models.admin_config_faces_dto import AdminConfigFacesDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigFacesDto from a JSON string
admin_config_faces_dto_instance = AdminConfigFacesDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigFacesDto.to_json())

# convert the object into a dict
admin_config_faces_dto_dict = admin_config_faces_dto_instance.to_dict()
# create an instance of AdminConfigFacesDto from a dict
admin_config_faces_dto_from_dict = AdminConfigFacesDto.from_dict(admin_config_faces_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



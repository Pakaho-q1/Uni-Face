# AdminConfigMetadataDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**faces** | [**AdminConfigFacesDto**](AdminConfigFacesDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_metadata_dto import AdminConfigMetadataDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigMetadataDto from a JSON string
admin_config_metadata_dto_instance = AdminConfigMetadataDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigMetadataDto.to_json())

# convert the object into a dict
admin_config_metadata_dto_dict = admin_config_metadata_dto_instance.to_dict()
# create an instance of AdminConfigMetadataDto from a dict
admin_config_metadata_dto_from_dict = AdminConfigMetadataDto.from_dict(admin_config_metadata_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



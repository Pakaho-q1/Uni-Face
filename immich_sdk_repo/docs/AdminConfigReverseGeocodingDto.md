# AdminConfigReverseGeocodingDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_reverse_geocoding_dto import AdminConfigReverseGeocodingDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigReverseGeocodingDto from a JSON string
admin_config_reverse_geocoding_dto_instance = AdminConfigReverseGeocodingDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigReverseGeocodingDto.to_json())

# convert the object into a dict
admin_config_reverse_geocoding_dto_dict = admin_config_reverse_geocoding_dto_instance.to_dict()
# create an instance of AdminConfigReverseGeocodingDto from a dict
admin_config_reverse_geocoding_dto_from_dict = AdminConfigReverseGeocodingDto.from_dict(admin_config_reverse_geocoding_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



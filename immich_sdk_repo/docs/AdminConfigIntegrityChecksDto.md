# AdminConfigIntegrityChecksDto

Integrity checks config

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum_files** | [**AdminConfigIntegrityChecksumJobDto**](AdminConfigIntegrityChecksumJobDto.md) |  | 
**missing_files** | [**AdminConfigIntegrityJobDto**](AdminConfigIntegrityJobDto.md) |  | 
**untracked_files** | [**AdminConfigIntegrityJobDto**](AdminConfigIntegrityJobDto.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_integrity_checks_dto import AdminConfigIntegrityChecksDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigIntegrityChecksDto from a JSON string
admin_config_integrity_checks_dto_instance = AdminConfigIntegrityChecksDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigIntegrityChecksDto.to_json())

# convert the object into a dict
admin_config_integrity_checks_dto_dict = admin_config_integrity_checks_dto_instance.to_dict()
# create an instance of AdminConfigIntegrityChecksDto from a dict
admin_config_integrity_checks_dto_from_dict = AdminConfigIntegrityChecksDto.from_dict(admin_config_integrity_checks_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



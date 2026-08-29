# AdminConfigIntegrityChecksumJobDto

Integrity checksum job config

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron_expression** | **str** | Cron expression for when the integrity check should run | 
**enabled** | **bool** | Enabled | 
**percentage_limit** | **float** | Percentage limit of the integrity checksum job | 
**time_limit** | **int** | How long the integrity checksum job may run for | 

## Example

```python
from immich_sdk.models.admin_config_integrity_checksum_job_dto import AdminConfigIntegrityChecksumJobDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigIntegrityChecksumJobDto from a JSON string
admin_config_integrity_checksum_job_dto_instance = AdminConfigIntegrityChecksumJobDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigIntegrityChecksumJobDto.to_json())

# convert the object into a dict
admin_config_integrity_checksum_job_dto_dict = admin_config_integrity_checksum_job_dto_instance.to_dict()
# create an instance of AdminConfigIntegrityChecksumJobDto from a dict
admin_config_integrity_checksum_job_dto_from_dict = AdminConfigIntegrityChecksumJobDto.from_dict(admin_config_integrity_checksum_job_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



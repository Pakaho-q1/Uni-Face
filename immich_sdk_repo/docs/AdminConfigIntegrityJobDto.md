# AdminConfigIntegrityJobDto

Integrity job config

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron_expression** | **str** | Cron expression for when the integrity check should run | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.admin_config_integrity_job_dto import AdminConfigIntegrityJobDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigIntegrityJobDto from a JSON string
admin_config_integrity_job_dto_instance = AdminConfigIntegrityJobDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigIntegrityJobDto.to_json())

# convert the object into a dict
admin_config_integrity_job_dto_dict = admin_config_integrity_job_dto_instance.to_dict()
# create an instance of AdminConfigIntegrityJobDto from a dict
admin_config_integrity_job_dto_from_dict = AdminConfigIntegrityJobDto.from_dict(admin_config_integrity_job_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



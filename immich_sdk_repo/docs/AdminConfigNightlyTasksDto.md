# AdminConfigNightlyTasksDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_new_faces** | **bool** | Cluster new faces | 
**database_cleanup** | **bool** | Database cleanup | 
**generate_memories** | **bool** | Generate memories | 
**missing_thumbnails** | **bool** | Missing thumbnails | 
**start_time** | **str** | Start time (HH:MM) | 
**sync_quota_usage** | **bool** | Sync quota usage | 

## Example

```python
from immich_sdk.models.admin_config_nightly_tasks_dto import AdminConfigNightlyTasksDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigNightlyTasksDto from a JSON string
admin_config_nightly_tasks_dto_instance = AdminConfigNightlyTasksDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigNightlyTasksDto.to_json())

# convert the object into a dict
admin_config_nightly_tasks_dto_dict = admin_config_nightly_tasks_dto_instance.to_dict()
# create an instance of AdminConfigNightlyTasksDto from a dict
admin_config_nightly_tasks_dto_from_dict = AdminConfigNightlyTasksDto.from_dict(admin_config_nightly_tasks_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



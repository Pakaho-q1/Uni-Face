# AdminConfigDuplicateDetectionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 
**max_distance** | **float** | Maximum distance threshold for duplicate detection | 

## Example

```python
from immich_sdk.models.admin_config_duplicate_detection_dto import AdminConfigDuplicateDetectionDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigDuplicateDetectionDto from a JSON string
admin_config_duplicate_detection_dto_instance = AdminConfigDuplicateDetectionDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigDuplicateDetectionDto.to_json())

# convert the object into a dict
admin_config_duplicate_detection_dto_dict = admin_config_duplicate_detection_dto_instance.to_dict()
# create an instance of AdminConfigDuplicateDetectionDto from a dict
admin_config_duplicate_detection_dto_from_dict = AdminConfigDuplicateDetectionDto.from_dict(admin_config_duplicate_detection_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



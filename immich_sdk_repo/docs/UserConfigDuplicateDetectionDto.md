# UserConfigDuplicateDetectionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 

## Example

```python
from immich_sdk.models.user_config_duplicate_detection_dto import UserConfigDuplicateDetectionDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigDuplicateDetectionDto from a JSON string
user_config_duplicate_detection_dto_instance = UserConfigDuplicateDetectionDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigDuplicateDetectionDto.to_json())

# convert the object into a dict
user_config_duplicate_detection_dto_dict = user_config_duplicate_detection_dto_instance.to_dict()
# create an instance of UserConfigDuplicateDetectionDto from a dict
user_config_duplicate_detection_dto_from_dict = UserConfigDuplicateDetectionDto.from_dict(user_config_duplicate_detection_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



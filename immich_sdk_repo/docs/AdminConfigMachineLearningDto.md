# AdminConfigMachineLearningDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**availability_checks** | [**AdminConfigMachineLearningAvailabilityChecksDto**](AdminConfigMachineLearningAvailabilityChecksDto.md) |  | 
**clip** | [**AdminConfigClipDto**](AdminConfigClipDto.md) |  | 
**duplicate_detection** | [**AdminConfigDuplicateDetectionDto**](AdminConfigDuplicateDetectionDto.md) |  | 
**enabled** | **bool** | Enabled | 
**facial_recognition** | [**AdminConfigFacialRecognitionDto**](AdminConfigFacialRecognitionDto.md) |  | 
**ocr** | [**AdminConfigOcrDto**](AdminConfigOcrDto.md) |  | 
**urls** | **List[str]** | ML service URLs | 

## Example

```python
from immich_sdk.models.admin_config_machine_learning_dto import AdminConfigMachineLearningDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigMachineLearningDto from a JSON string
admin_config_machine_learning_dto_instance = AdminConfigMachineLearningDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigMachineLearningDto.to_json())

# convert the object into a dict
admin_config_machine_learning_dto_dict = admin_config_machine_learning_dto_instance.to_dict()
# create an instance of AdminConfigMachineLearningDto from a dict
admin_config_machine_learning_dto_from_dict = AdminConfigMachineLearningDto.from_dict(admin_config_machine_learning_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



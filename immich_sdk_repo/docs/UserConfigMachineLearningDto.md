# UserConfigMachineLearningDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**clip** | [**UserConfigClipDto**](UserConfigClipDto.md) |  | 
**duplicate_detection** | [**UserConfigDuplicateDetectionDto**](UserConfigDuplicateDetectionDto.md) |  | 
**enabled** | **bool** | Enabled | 
**facial_recognition** | [**UserConfigFacialRecognitionDto**](UserConfigFacialRecognitionDto.md) |  | 
**ocr** | [**UserConfigOcrDto**](UserConfigOcrDto.md) |  | 

## Example

```python
from immich_sdk.models.user_config_machine_learning_dto import UserConfigMachineLearningDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigMachineLearningDto from a JSON string
user_config_machine_learning_dto_instance = UserConfigMachineLearningDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigMachineLearningDto.to_json())

# convert the object into a dict
user_config_machine_learning_dto_dict = user_config_machine_learning_dto_instance.to_dict()
# create an instance of UserConfigMachineLearningDto from a dict
user_config_machine_learning_dto_from_dict = UserConfigMachineLearningDto.from_dict(user_config_machine_learning_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



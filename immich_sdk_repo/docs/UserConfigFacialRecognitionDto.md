# UserConfigFacialRecognitionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 
**min_faces** | **int** | Minimum number of faces required for recognition | 

## Example

```python
from immich_sdk.models.user_config_facial_recognition_dto import UserConfigFacialRecognitionDto

# TODO update the JSON string below
json = "{}"
# create an instance of UserConfigFacialRecognitionDto from a JSON string
user_config_facial_recognition_dto_instance = UserConfigFacialRecognitionDto.from_json(json)
# print the JSON string representation of the object
print(UserConfigFacialRecognitionDto.to_json())

# convert the object into a dict
user_config_facial_recognition_dto_dict = user_config_facial_recognition_dto_instance.to_dict()
# create an instance of UserConfigFacialRecognitionDto from a dict
user_config_facial_recognition_dto_from_dict = UserConfigFacialRecognitionDto.from_dict(user_config_facial_recognition_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



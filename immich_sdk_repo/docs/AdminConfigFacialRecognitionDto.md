# AdminConfigFacialRecognitionDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 
**max_distance** | **float** | Maximum distance threshold for face recognition | 
**min_faces** | **int** | Minimum number of faces required for recognition | 
**min_score** | **float** | Minimum confidence score for face detection | 
**model_name** | **str** | Name of the model to use | 

## Example

```python
from immich_sdk.models.admin_config_facial_recognition_dto import AdminConfigFacialRecognitionDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigFacialRecognitionDto from a JSON string
admin_config_facial_recognition_dto_instance = AdminConfigFacialRecognitionDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigFacialRecognitionDto.to_json())

# convert the object into a dict
admin_config_facial_recognition_dto_dict = admin_config_facial_recognition_dto_instance.to_dict()
# create an instance of AdminConfigFacialRecognitionDto from a dict
admin_config_facial_recognition_dto_from_dict = AdminConfigFacialRecognitionDto.from_dict(admin_config_facial_recognition_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



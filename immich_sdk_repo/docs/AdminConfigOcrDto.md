# AdminConfigOcrDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether the task is enabled | 
**max_resolution** | **int** | Maximum resolution for OCR processing | 
**min_detection_score** | **float** | Minimum confidence score for text detection | 
**min_recognition_score** | **float** | Minimum confidence score for text recognition | 
**model_name** | **str** | Name of the model to use | 

## Example

```python
from immich_sdk.models.admin_config_ocr_dto import AdminConfigOcrDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigOcrDto from a JSON string
admin_config_ocr_dto_instance = AdminConfigOcrDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigOcrDto.to_json())

# convert the object into a dict
admin_config_ocr_dto_dict = admin_config_ocr_dto_instance.to_dict()
# create an instance of AdminConfigOcrDto from a dict
admin_config_ocr_dto_from_dict = AdminConfigOcrDto.from_dict(admin_config_ocr_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



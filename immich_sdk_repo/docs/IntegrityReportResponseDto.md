# IntegrityReportResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[IntegrityReportResponseDtoItemsInner]**](IntegrityReportResponseDtoItemsInner.md) |  | 
**next_cursor** | **str** |  | [optional] 

## Example

```python
from immich_sdk.models.integrity_report_response_dto import IntegrityReportResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of IntegrityReportResponseDto from a JSON string
integrity_report_response_dto_instance = IntegrityReportResponseDto.from_json(json)
# print the JSON string representation of the object
print(IntegrityReportResponseDto.to_json())

# convert the object into a dict
integrity_report_response_dto_dict = integrity_report_response_dto_instance.to_dict()
# create an instance of IntegrityReportResponseDto from a dict
integrity_report_response_dto_from_dict = IntegrityReportResponseDto.from_dict(integrity_report_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



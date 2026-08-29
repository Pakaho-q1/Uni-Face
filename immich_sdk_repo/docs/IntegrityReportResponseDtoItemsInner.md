# IntegrityReportResponseDtoItemsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | Integrity report item id | 
**path** | **str** | Integrity report item path | 
**type** | [**IntegrityReport**](IntegrityReport.md) |  | 

## Example

```python
from immich_sdk.models.integrity_report_response_dto_items_inner import IntegrityReportResponseDtoItemsInner

# TODO update the JSON string below
json = "{}"
# create an instance of IntegrityReportResponseDtoItemsInner from a JSON string
integrity_report_response_dto_items_inner_instance = IntegrityReportResponseDtoItemsInner.from_json(json)
# print the JSON string representation of the object
print(IntegrityReportResponseDtoItemsInner.to_json())

# convert the object into a dict
integrity_report_response_dto_items_inner_dict = integrity_report_response_dto_items_inner_instance.to_dict()
# create an instance of IntegrityReportResponseDtoItemsInner from a dict
integrity_report_response_dto_items_inner_from_dict = IntegrityReportResponseDtoItemsInner.from_dict(integrity_report_response_dto_items_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



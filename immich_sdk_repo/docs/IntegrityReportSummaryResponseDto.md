# IntegrityReportSummaryResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**checksum_mismatch** | **int** |  | 
**missing_file** | **int** |  | 
**untracked_file** | **int** |  | 

## Example

```python
from immich_sdk.models.integrity_report_summary_response_dto import IntegrityReportSummaryResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of IntegrityReportSummaryResponseDto from a JSON string
integrity_report_summary_response_dto_instance = IntegrityReportSummaryResponseDto.from_json(json)
# print the JSON string representation of the object
print(IntegrityReportSummaryResponseDto.to_json())

# convert the object into a dict
integrity_report_summary_response_dto_dict = integrity_report_summary_response_dto_instance.to_dict()
# create an instance of IntegrityReportSummaryResponseDto from a dict
integrity_report_summary_response_dto_from_dict = IntegrityReportSummaryResponseDto.from_dict(integrity_report_summary_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



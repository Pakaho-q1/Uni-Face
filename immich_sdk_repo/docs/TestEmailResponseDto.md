# TestEmailResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message_id** | **str** | Email message ID | 

## Example

```python
from immich_sdk.models.test_email_response_dto import TestEmailResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of TestEmailResponseDto from a JSON string
test_email_response_dto_instance = TestEmailResponseDto.from_json(json)
# print the JSON string representation of the object
print(TestEmailResponseDto.to_json())

# convert the object into a dict
test_email_response_dto_dict = test_email_response_dto_instance.to_dict()
# create an instance of TestEmailResponseDto from a dict
test_email_response_dto_from_dict = TestEmailResponseDto.from_dict(test_email_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



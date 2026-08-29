# PinCodeResetDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**password** | **str** | User password (required if PIN code is not provided) | [optional] 
**pin_code** | **str** | New PIN code (4-6 digits) | [optional] 

## Example

```python
from immich_sdk.models.pin_code_reset_dto import PinCodeResetDto

# TODO update the JSON string below
json = "{}"
# create an instance of PinCodeResetDto from a JSON string
pin_code_reset_dto_instance = PinCodeResetDto.from_json(json)
# print the JSON string representation of the object
print(PinCodeResetDto.to_json())

# convert the object into a dict
pin_code_reset_dto_dict = pin_code_reset_dto_instance.to_dict()
# create an instance of PinCodeResetDto from a dict
pin_code_reset_dto_from_dict = PinCodeResetDto.from_dict(pin_code_reset_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



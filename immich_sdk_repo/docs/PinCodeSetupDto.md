# PinCodeSetupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pin_code** | **str** | PIN code (4-6 digits) | 

## Example

```python
from immich_sdk.models.pin_code_setup_dto import PinCodeSetupDto

# TODO update the JSON string below
json = "{}"
# create an instance of PinCodeSetupDto from a JSON string
pin_code_setup_dto_instance = PinCodeSetupDto.from_json(json)
# print the JSON string representation of the object
print(PinCodeSetupDto.to_json())

# convert the object into a dict
pin_code_setup_dto_dict = pin_code_setup_dto_instance.to_dict()
# create an instance of PinCodeSetupDto from a dict
pin_code_setup_dto_from_dict = PinCodeSetupDto.from_dict(pin_code_setup_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



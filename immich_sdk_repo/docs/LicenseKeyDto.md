# LicenseKeyDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**activation_key** | **str** | Activation key | 
**license_key** | **str** | License key (format: /^IM(SV|CL)(-[\\dA-Za-z]{4}){8}$/) | 

## Example

```python
from immich_sdk.models.license_key_dto import LicenseKeyDto

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseKeyDto from a JSON string
license_key_dto_instance = LicenseKeyDto.from_json(json)
# print the JSON string representation of the object
print(LicenseKeyDto.to_json())

# convert the object into a dict
license_key_dto_dict = license_key_dto_instance.to_dict()
# create an instance of LicenseKeyDto from a dict
license_key_dto_from_dict = LicenseKeyDto.from_dict(license_key_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



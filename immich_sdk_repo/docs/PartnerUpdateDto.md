# PartnerUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**in_timeline** | **bool** | Show partner assets in timeline | 

## Example

```python
from immich_sdk.models.partner_update_dto import PartnerUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of PartnerUpdateDto from a JSON string
partner_update_dto_instance = PartnerUpdateDto.from_json(json)
# print the JSON string representation of the object
print(PartnerUpdateDto.to_json())

# convert the object into a dict
partner_update_dto_dict = partner_update_dto_instance.to_dict()
# create an instance of PartnerUpdateDto from a dict
partner_update_dto_from_dict = PartnerUpdateDto.from_dict(partner_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



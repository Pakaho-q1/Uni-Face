# PartnerCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_with_id** | **UUID** | User ID to share with | 

## Example

```python
from immich_sdk.models.partner_create_dto import PartnerCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of PartnerCreateDto from a JSON string
partner_create_dto_instance = PartnerCreateDto.from_json(json)
# print the JSON string representation of the object
print(PartnerCreateDto.to_json())

# convert the object into a dict
partner_create_dto_dict = partner_create_dto_instance.to_dict()
# create an instance of PartnerCreateDto from a dict
partner_create_dto_from_dict = PartnerCreateDto.from_dict(partner_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



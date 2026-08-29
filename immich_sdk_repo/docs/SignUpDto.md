# SignUpDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | User email | 
**name** | **str** | User name | 
**password** | **str** | User password | 

## Example

```python
from immich_sdk.models.sign_up_dto import SignUpDto

# TODO update the JSON string below
json = "{}"
# create an instance of SignUpDto from a JSON string
sign_up_dto_instance = SignUpDto.from_json(json)
# print the JSON string representation of the object
print(SignUpDto.to_json())

# convert the object into a dict
sign_up_dto_dict = sign_up_dto_instance.to_dict()
# create an instance of SignUpDto from a dict
sign_up_dto_from_dict = SignUpDto.from_dict(sign_up_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



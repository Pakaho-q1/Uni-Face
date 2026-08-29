# ApiKeyCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | API key name | [optional] 
**permissions** | [**List[Permission]**](Permission.md) | List of permissions | 

## Example

```python
from immich_sdk.models.api_key_create_dto import ApiKeyCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of ApiKeyCreateDto from a JSON string
api_key_create_dto_instance = ApiKeyCreateDto.from_json(json)
# print the JSON string representation of the object
print(ApiKeyCreateDto.to_json())

# convert the object into a dict
api_key_create_dto_dict = api_key_create_dto_instance.to_dict()
# create an instance of ApiKeyCreateDto from a dict
api_key_create_dto_from_dict = ApiKeyCreateDto.from_dict(api_key_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



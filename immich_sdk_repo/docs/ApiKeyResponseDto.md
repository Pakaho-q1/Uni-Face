# ApiKeyResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | Creation date | 
**id** | **UUID** | API key ID | 
**name** | **str** | API key name | 
**permissions** | [**List[Permission]**](Permission.md) | List of permissions | 
**updated_at** | **datetime** | Last update date | 

## Example

```python
from immich_sdk.models.api_key_response_dto import ApiKeyResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ApiKeyResponseDto from a JSON string
api_key_response_dto_instance = ApiKeyResponseDto.from_json(json)
# print the JSON string representation of the object
print(ApiKeyResponseDto.to_json())

# convert the object into a dict
api_key_response_dto_dict = api_key_response_dto_instance.to_dict()
# create an instance of ApiKeyResponseDto from a dict
api_key_response_dto_from_dict = ApiKeyResponseDto.from_dict(api_key_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



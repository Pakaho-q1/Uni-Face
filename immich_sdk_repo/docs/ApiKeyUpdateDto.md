# ApiKeyUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | API key name | [optional] 
**permissions** | [**List[Permission]**](Permission.md) | List of permissions | [optional] 

## Example

```python
from immich_sdk.models.api_key_update_dto import ApiKeyUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of ApiKeyUpdateDto from a JSON string
api_key_update_dto_instance = ApiKeyUpdateDto.from_json(json)
# print the JSON string representation of the object
print(ApiKeyUpdateDto.to_json())

# convert the object into a dict
api_key_update_dto_dict = api_key_update_dto_instance.to_dict()
# create an instance of ApiKeyUpdateDto from a dict
api_key_update_dto_from_dict = ApiKeyUpdateDto.from_dict(api_key_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# PublicConfigServerDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**login_page_message** | **str** | Login page message | 

## Example

```python
from immich_sdk.models.public_config_server_dto import PublicConfigServerDto

# TODO update the JSON string below
json = "{}"
# create an instance of PublicConfigServerDto from a JSON string
public_config_server_dto_instance = PublicConfigServerDto.from_json(json)
# print the JSON string representation of the object
print(PublicConfigServerDto.to_json())

# convert the object into a dict
public_config_server_dto_dict = public_config_server_dto_instance.to_dict()
# create an instance of PublicConfigServerDto from a dict
public_config_server_dto_from_dict = PublicConfigServerDto.from_dict(public_config_server_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



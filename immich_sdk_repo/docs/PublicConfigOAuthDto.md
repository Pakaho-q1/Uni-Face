# PublicConfigOAuthDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_launch** | **bool** | Auto launch | 
**button_text** | **str** | Button text | 
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.public_config_o_auth_dto import PublicConfigOAuthDto

# TODO update the JSON string below
json = "{}"
# create an instance of PublicConfigOAuthDto from a JSON string
public_config_o_auth_dto_instance = PublicConfigOAuthDto.from_json(json)
# print the JSON string representation of the object
print(PublicConfigOAuthDto.to_json())

# convert the object into a dict
public_config_o_auth_dto_dict = public_config_o_auth_dto_instance.to_dict()
# create an instance of PublicConfigOAuthDto from a dict
public_config_o_auth_dto_from_dict = PublicConfigOAuthDto.from_dict(public_config_o_auth_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



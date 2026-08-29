# PublicConfigPasswordLoginDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 

## Example

```python
from immich_sdk.models.public_config_password_login_dto import PublicConfigPasswordLoginDto

# TODO update the JSON string below
json = "{}"
# create an instance of PublicConfigPasswordLoginDto from a JSON string
public_config_password_login_dto_instance = PublicConfigPasswordLoginDto.from_json(json)
# print the JSON string representation of the object
print(PublicConfigPasswordLoginDto.to_json())

# convert the object into a dict
public_config_password_login_dto_dict = public_config_password_login_dto_instance.to_dict()
# create an instance of PublicConfigPasswordLoginDto from a dict
public_config_password_login_dto_from_dict = PublicConfigPasswordLoginDto.from_dict(public_config_password_login_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



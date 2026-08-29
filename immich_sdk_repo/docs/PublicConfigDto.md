# PublicConfigDto

Configuration properties that are visible to everyone

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**oauth** | [**PublicConfigOAuthDto**](PublicConfigOAuthDto.md) |  | 
**password_login** | [**PublicConfigPasswordLoginDto**](PublicConfigPasswordLoginDto.md) |  | 
**server** | [**PublicConfigServerDto**](PublicConfigServerDto.md) |  | 
**theme** | [**PublicConfigThemeDto**](PublicConfigThemeDto.md) |  | 

## Example

```python
from immich_sdk.models.public_config_dto import PublicConfigDto

# TODO update the JSON string below
json = "{}"
# create an instance of PublicConfigDto from a JSON string
public_config_dto_instance = PublicConfigDto.from_json(json)
# print the JSON string representation of the object
print(PublicConfigDto.to_json())

# convert the object into a dict
public_config_dto_dict = public_config_dto_instance.to_dict()
# create an instance of PublicConfigDto from a dict
public_config_dto_from_dict = PublicConfigDto.from_dict(public_config_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



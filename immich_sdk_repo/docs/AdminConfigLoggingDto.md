# AdminConfigLoggingDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 
**level** | [**LogLevel**](LogLevel.md) |  | 

## Example

```python
from immich_sdk.models.admin_config_logging_dto import AdminConfigLoggingDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigLoggingDto from a JSON string
admin_config_logging_dto_instance = AdminConfigLoggingDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigLoggingDto.to_json())

# convert the object into a dict
admin_config_logging_dto_dict = admin_config_logging_dto_instance.to_dict()
# create an instance of AdminConfigLoggingDto from a dict
admin_config_logging_dto_from_dict = AdminConfigLoggingDto.from_dict(admin_config_logging_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



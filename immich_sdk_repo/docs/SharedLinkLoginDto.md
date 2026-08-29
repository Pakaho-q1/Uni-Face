# SharedLinkLoginDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**password** | **str** | Shared link password | 

## Example

```python
from immich_sdk.models.shared_link_login_dto import SharedLinkLoginDto

# TODO update the JSON string below
json = "{}"
# create an instance of SharedLinkLoginDto from a JSON string
shared_link_login_dto_instance = SharedLinkLoginDto.from_json(json)
# print the JSON string representation of the object
print(SharedLinkLoginDto.to_json())

# convert the object into a dict
shared_link_login_dto_dict = shared_link_login_dto_instance.to_dict()
# create an instance of SharedLinkLoginDto from a dict
shared_link_login_dto_from_dict = SharedLinkLoginDto.from_dict(shared_link_login_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# AvatarUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | [**UserAvatarColor**](UserAvatarColor.md) |  | [optional] 

## Example

```python
from immich_sdk.models.avatar_update import AvatarUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of AvatarUpdate from a JSON string
avatar_update_instance = AvatarUpdate.from_json(json)
# print the JSON string representation of the object
print(AvatarUpdate.to_json())

# convert the object into a dict
avatar_update_dict = avatar_update_instance.to_dict()
# create an instance of AvatarUpdate from a dict
avatar_update_from_dict = AvatarUpdate.from_dict(avatar_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



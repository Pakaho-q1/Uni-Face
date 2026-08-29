# RecentlyAddedUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sidebar_web** | **bool** | Whether the recently added page appears in the web sidebar | [optional] 

## Example

```python
from immich_sdk.models.recently_added_update import RecentlyAddedUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of RecentlyAddedUpdate from a JSON string
recently_added_update_instance = RecentlyAddedUpdate.from_json(json)
# print the JSON string representation of the object
print(RecentlyAddedUpdate.to_json())

# convert the object into a dict
recently_added_update_dict = recently_added_update_instance.to_dict()
# create an instance of RecentlyAddedUpdate from a dict
recently_added_update_from_dict = RecentlyAddedUpdate.from_dict(recently_added_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



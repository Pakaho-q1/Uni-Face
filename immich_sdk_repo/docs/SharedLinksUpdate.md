# SharedLinksUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether shared links are enabled | [optional] 
**sidebar_web** | **bool** | Whether shared links appear in web sidebar | [optional] 

## Example

```python
from immich_sdk.models.shared_links_update import SharedLinksUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of SharedLinksUpdate from a JSON string
shared_links_update_instance = SharedLinksUpdate.from_json(json)
# print the JSON string representation of the object
print(SharedLinksUpdate.to_json())

# convert the object into a dict
shared_links_update_dict = shared_links_update_instance.to_dict()
# create an instance of SharedLinksUpdate from a dict
shared_links_update_from_dict = SharedLinksUpdate.from_dict(shared_links_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# TagsUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether tags are enabled | [optional] 
**sidebar_web** | **bool** | Whether tags appear in web sidebar | [optional] 

## Example

```python
from immich_sdk.models.tags_update import TagsUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of TagsUpdate from a JSON string
tags_update_instance = TagsUpdate.from_json(json)
# print the JSON string representation of the object
print(TagsUpdate.to_json())

# convert the object into a dict
tags_update_dict = tags_update_instance.to_dict()
# create an instance of TagsUpdate from a dict
tags_update_from_dict = TagsUpdate.from_dict(tags_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



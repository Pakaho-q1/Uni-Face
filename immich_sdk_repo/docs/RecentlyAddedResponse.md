# RecentlyAddedResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sidebar_web** | **bool** | Whether the recently added page appears in the web sidebar | 

## Example

```python
from immich_sdk.models.recently_added_response import RecentlyAddedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RecentlyAddedResponse from a JSON string
recently_added_response_instance = RecentlyAddedResponse.from_json(json)
# print the JSON string representation of the object
print(RecentlyAddedResponse.to_json())

# convert the object into a dict
recently_added_response_dict = recently_added_response_instance.to_dict()
# create an instance of RecentlyAddedResponse from a dict
recently_added_response_from_dict = RecentlyAddedResponse.from_dict(recently_added_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



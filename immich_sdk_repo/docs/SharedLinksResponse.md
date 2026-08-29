# SharedLinksResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether shared links are enabled | 
**sidebar_web** | **bool** | Whether shared links appear in web sidebar | 

## Example

```python
from immich_sdk.models.shared_links_response import SharedLinksResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedLinksResponse from a JSON string
shared_links_response_instance = SharedLinksResponse.from_json(json)
# print the JSON string representation of the object
print(SharedLinksResponse.to_json())

# convert the object into a dict
shared_links_response_dict = shared_links_response_instance.to_dict()
# create an instance of SharedLinksResponse from a dict
shared_links_response_from_dict = SharedLinksResponse.from_dict(shared_links_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



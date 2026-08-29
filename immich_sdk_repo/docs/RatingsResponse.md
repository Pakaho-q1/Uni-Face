# RatingsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether ratings are enabled | 

## Example

```python
from immich_sdk.models.ratings_response import RatingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RatingsResponse from a JSON string
ratings_response_instance = RatingsResponse.from_json(json)
# print the JSON string representation of the object
print(RatingsResponse.to_json())

# convert the object into a dict
ratings_response_dict = ratings_response_instance.to_dict()
# create an instance of RatingsResponse from a dict
ratings_response_from_dict = RatingsResponse.from_dict(ratings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



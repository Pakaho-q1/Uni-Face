# RatingsUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether ratings are enabled | [optional] 

## Example

```python
from immich_sdk.models.ratings_update import RatingsUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of RatingsUpdate from a JSON string
ratings_update_instance = RatingsUpdate.from_json(json)
# print the JSON string representation of the object
print(RatingsUpdate.to_json())

# convert the object into a dict
ratings_update_dict = ratings_update_instance.to_dict()
# create an instance of RatingsUpdate from a dict
ratings_update_from_dict = RatingsUpdate.from_dict(ratings_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



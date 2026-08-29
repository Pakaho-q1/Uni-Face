# StringSimilarityFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**matches** | **str** |  | 

## Example

```python
from immich_sdk.models.string_similarity_filter import StringSimilarityFilter

# TODO update the JSON string below
json = "{}"
# create an instance of StringSimilarityFilter from a JSON string
string_similarity_filter_instance = StringSimilarityFilter.from_json(json)
# print the JSON string representation of the object
print(StringSimilarityFilter.to_json())

# convert the object into a dict
string_similarity_filter_dict = string_similarity_filter_instance.to_dict()
# create an instance of StringSimilarityFilter from a dict
string_similarity_filter_from_dict = StringSimilarityFilter.from_dict(string_similarity_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



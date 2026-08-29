# SearchStatisticsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Total number of matching assets | 

## Example

```python
from immich_sdk.models.search_statistics_response_dto import SearchStatisticsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of SearchStatisticsResponseDto from a JSON string
search_statistics_response_dto_instance = SearchStatisticsResponseDto.from_json(json)
# print the JSON string representation of the object
print(SearchStatisticsResponseDto.to_json())

# convert the object into a dict
search_statistics_response_dto_dict = search_statistics_response_dto_instance.to_dict()
# create an instance of SearchStatisticsResponseDto from a dict
search_statistics_response_dto_from_dict = SearchStatisticsResponseDto.from_dict(search_statistics_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



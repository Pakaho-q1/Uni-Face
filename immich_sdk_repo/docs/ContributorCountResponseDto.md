# ContributorCountResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_count** | **int** | Number of assets contributed | 
**user_id** | **UUID** | User ID | 

## Example

```python
from immich_sdk.models.contributor_count_response_dto import ContributorCountResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ContributorCountResponseDto from a JSON string
contributor_count_response_dto_instance = ContributorCountResponseDto.from_json(json)
# print the JSON string representation of the object
print(ContributorCountResponseDto.to_json())

# convert the object into a dict
contributor_count_response_dto_dict = contributor_count_response_dto_instance.to_dict()
# create an instance of ContributorCountResponseDto from a dict
contributor_count_response_dto_from_dict = ContributorCountResponseDto.from_dict(contributor_count_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



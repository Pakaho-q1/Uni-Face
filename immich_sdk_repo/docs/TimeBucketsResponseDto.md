# TimeBucketsResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of assets in this time bucket | 
**time_bucket** | **str** | Time bucket identifier in YYYY-MM-DD format representing the start of the time period | 

## Example

```python
from immich_sdk.models.time_buckets_response_dto import TimeBucketsResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of TimeBucketsResponseDto from a JSON string
time_buckets_response_dto_instance = TimeBucketsResponseDto.from_json(json)
# print the JSON string representation of the object
print(TimeBucketsResponseDto.to_json())

# convert the object into a dict
time_buckets_response_dto_dict = time_buckets_response_dto_instance.to_dict()
# create an instance of TimeBucketsResponseDto from a dict
time_buckets_response_dto_from_dict = TimeBucketsResponseDto.from_dict(time_buckets_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



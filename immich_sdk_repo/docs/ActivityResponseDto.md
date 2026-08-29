# ActivityResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_id** | **UUID** | Asset ID (if activity is for an asset) | 
**comment** | **str** | Comment text (for comment activities) | [optional] 
**created_at** | **datetime** | Creation date | 
**id** | **UUID** | Activity ID | 
**type** | [**ReactionType**](ReactionType.md) |  | 
**user** | [**UserResponseDto**](UserResponseDto.md) |  | 

## Example

```python
from immich_sdk.models.activity_response_dto import ActivityResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ActivityResponseDto from a JSON string
activity_response_dto_instance = ActivityResponseDto.from_json(json)
# print the JSON string representation of the object
print(ActivityResponseDto.to_json())

# convert the object into a dict
activity_response_dto_dict = activity_response_dto_instance.to_dict()
# create an instance of ActivityResponseDto from a dict
activity_response_dto_from_dict = ActivityResponseDto.from_dict(activity_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



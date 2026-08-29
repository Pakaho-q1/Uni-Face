# TagResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** | Tag color (hex) | [optional] 
**created_at** | **datetime** | Creation date | 
**id** | **UUID** | Tag ID | 
**name** | **str** | Tag name | 
**parent_id** | **str** | Parent tag ID | [optional] 
**updated_at** | **datetime** | Last update date | 
**value** | **str** | Tag value (full path) | 

## Example

```python
from immich_sdk.models.tag_response_dto import TagResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of TagResponseDto from a JSON string
tag_response_dto_instance = TagResponseDto.from_json(json)
# print the JSON string representation of the object
print(TagResponseDto.to_json())

# convert the object into a dict
tag_response_dto_dict = tag_response_dto_instance.to_dict()
# create an instance of TagResponseDto from a dict
tag_response_dto_from_dict = TagResponseDto.from_dict(tag_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



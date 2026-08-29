# TagCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** | Tag color (hex) | [optional] 
**name** | **str** | Tag name | 
**parent_id** | **UUID** | Parent tag ID | [optional] 

## Example

```python
from immich_sdk.models.tag_create_dto import TagCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of TagCreateDto from a JSON string
tag_create_dto_instance = TagCreateDto.from_json(json)
# print the JSON string representation of the object
print(TagCreateDto.to_json())

# convert the object into a dict
tag_create_dto_dict = tag_create_dto_instance.to_dict()
# create an instance of TagCreateDto from a dict
tag_create_dto_from_dict = TagCreateDto.from_dict(tag_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



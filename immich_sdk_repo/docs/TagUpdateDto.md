# TagUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** | Tag color (hex) | [optional] 
**name** | **str** | Tag name | [optional] 

## Example

```python
from immich_sdk.models.tag_update_dto import TagUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of TagUpdateDto from a JSON string
tag_update_dto_instance = TagUpdateDto.from_json(json)
# print the JSON string representation of the object
print(TagUpdateDto.to_json())

# convert the object into a dict
tag_update_dto_dict = tag_update_dto_instance.to_dict()
# create an instance of TagUpdateDto from a dict
tag_update_dto_from_dict = TagUpdateDto.from_dict(tag_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# TagUpsertDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tags** | **List[str]** | Tag names to upsert | 

## Example

```python
from immich_sdk.models.tag_upsert_dto import TagUpsertDto

# TODO update the JSON string below
json = "{}"
# create an instance of TagUpsertDto from a JSON string
tag_upsert_dto_instance = TagUpsertDto.from_json(json)
# print the JSON string representation of the object
print(TagUpsertDto.to_json())

# convert the object into a dict
tag_upsert_dto_dict = tag_upsert_dto_instance.to_dict()
# create an instance of TagUpsertDto from a dict
tag_upsert_dto_from_dict = TagUpsertDto.from_dict(tag_upsert_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



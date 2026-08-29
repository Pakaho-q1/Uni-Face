# DuplicateResolveGroupDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**duplicate_id** | **UUID** |  | 
**keep_asset_ids** | **List[UUID]** | Asset IDs to keep | 
**trash_asset_ids** | **List[UUID]** | Asset IDs to trash or delete | 

## Example

```python
from immich_sdk.models.duplicate_resolve_group_dto import DuplicateResolveGroupDto

# TODO update the JSON string below
json = "{}"
# create an instance of DuplicateResolveGroupDto from a JSON string
duplicate_resolve_group_dto_instance = DuplicateResolveGroupDto.from_json(json)
# print the JSON string representation of the object
print(DuplicateResolveGroupDto.to_json())

# convert the object into a dict
duplicate_resolve_group_dto_dict = duplicate_resolve_group_dto_instance.to_dict()
# create an instance of DuplicateResolveGroupDto from a dict
duplicate_resolve_group_dto_from_dict = DuplicateResolveGroupDto.from_dict(duplicate_resolve_group_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



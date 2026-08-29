# DuplicateResolveDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**groups** | [**List[DuplicateResolveGroupDto]**](DuplicateResolveGroupDto.md) | List of duplicate groups to resolve | 

## Example

```python
from immich_sdk.models.duplicate_resolve_dto import DuplicateResolveDto

# TODO update the JSON string below
json = "{}"
# create an instance of DuplicateResolveDto from a JSON string
duplicate_resolve_dto_instance = DuplicateResolveDto.from_json(json)
# print the JSON string representation of the object
print(DuplicateResolveDto.to_json())

# convert the object into a dict
duplicate_resolve_dto_dict = duplicate_resolve_dto_instance.to_dict()
# create an instance of DuplicateResolveDto from a dict
duplicate_resolve_dto_from_dict = DuplicateResolveDto.from_dict(duplicate_resolve_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



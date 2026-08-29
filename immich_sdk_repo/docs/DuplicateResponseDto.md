# DuplicateResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assets** | [**List[AssetResponseDto]**](AssetResponseDto.md) | Duplicate assets | 
**duplicate_id** | **UUID** | Duplicate group ID | 
**suggested_keep_asset_ids** | **List[UUID]** | Suggested asset IDs to keep based on file size and EXIF data | 

## Example

```python
from immich_sdk.models.duplicate_response_dto import DuplicateResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of DuplicateResponseDto from a JSON string
duplicate_response_dto_instance = DuplicateResponseDto.from_json(json)
# print the JSON string representation of the object
print(DuplicateResponseDto.to_json())

# convert the object into a dict
duplicate_response_dto_dict = duplicate_response_dto_instance.to_dict()
# create an instance of DuplicateResponseDto from a dict
duplicate_response_dto_from_dict = DuplicateResponseDto.from_dict(duplicate_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



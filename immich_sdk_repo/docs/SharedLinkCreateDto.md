# SharedLinkCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_id** | **UUID** | Album ID (for album sharing) | [optional] 
**allow_download** | **bool** | Allow downloads | [optional] [default to True]
**allow_upload** | **bool** | Allow uploads | [optional] 
**asset_ids** | **List[UUID]** | Asset IDs (for individual assets) | [optional] 
**description** | **str** | Link description | [optional] 
**expires_at** | **datetime** | Expiration date | [optional] 
**password** | **str** | Link password | [optional] 
**show_metadata** | **bool** | Show metadata | [optional] [default to True]
**slug** | **str** | Custom URL slug | [optional] 
**type** | [**SharedLinkType**](SharedLinkType.md) |  | 

## Example

```python
from immich_sdk.models.shared_link_create_dto import SharedLinkCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of SharedLinkCreateDto from a JSON string
shared_link_create_dto_instance = SharedLinkCreateDto.from_json(json)
# print the JSON string representation of the object
print(SharedLinkCreateDto.to_json())

# convert the object into a dict
shared_link_create_dto_dict = shared_link_create_dto_instance.to_dict()
# create an instance of SharedLinkCreateDto from a dict
shared_link_create_dto_from_dict = SharedLinkCreateDto.from_dict(shared_link_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



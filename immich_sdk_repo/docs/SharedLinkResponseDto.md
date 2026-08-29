# SharedLinkResponseDto

Shared link response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album** | [**AlbumResponseDto**](AlbumResponseDto.md) |  | [optional] 
**allow_download** | **bool** | Allow downloads | 
**allow_upload** | **bool** | Allow uploads | 
**assets** | [**List[AssetResponseDto]**](AssetResponseDto.md) |  | 
**created_at** | **datetime** | Creation date | 
**description** | **str** | Link description | 
**expires_at** | **datetime** | Expiration date | 
**id** | **UUID** | Shared link ID | 
**key** | **str** | Encryption key (base64url) | 
**password** | **str** | Has password | 
**show_metadata** | **bool** | Show metadata | 
**slug** | **str** | Custom URL slug | 
**type** | [**SharedLinkType**](SharedLinkType.md) |  | 
**user_id** | **UUID** | Owner user ID | 

## Example

```python
from immich_sdk.models.shared_link_response_dto import SharedLinkResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of SharedLinkResponseDto from a JSON string
shared_link_response_dto_instance = SharedLinkResponseDto.from_json(json)
# print the JSON string representation of the object
print(SharedLinkResponseDto.to_json())

# convert the object into a dict
shared_link_response_dto_dict = shared_link_response_dto_instance.to_dict()
# create an instance of SharedLinkResponseDto from a dict
shared_link_response_dto_from_dict = SharedLinkResponseDto.from_dict(shared_link_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



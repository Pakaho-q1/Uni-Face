# SharedLinkEditDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allow_download** | **bool** | Allow downloads | [optional] 
**allow_upload** | **bool** | Allow uploads | [optional] 
**description** | **str** | Link description | [optional] 
**expires_at** | **datetime** | Expiration date | [optional] 
**password** | **str** | Link password | [optional] 
**show_metadata** | **bool** | Show metadata | [optional] 
**slug** | **str** | Custom URL slug | [optional] 

## Example

```python
from immich_sdk.models.shared_link_edit_dto import SharedLinkEditDto

# TODO update the JSON string below
json = "{}"
# create an instance of SharedLinkEditDto from a JSON string
shared_link_edit_dto_instance = SharedLinkEditDto.from_json(json)
# print the JSON string representation of the object
print(SharedLinkEditDto.to_json())

# convert the object into a dict
shared_link_edit_dto_dict = shared_link_edit_dto_instance.to_dict()
# create an instance of SharedLinkEditDto from a dict
shared_link_edit_dto_from_dict = SharedLinkEditDto.from_dict(shared_link_edit_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



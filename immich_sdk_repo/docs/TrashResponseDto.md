# TrashResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Number of items in trash | 

## Example

```python
from immich_sdk.models.trash_response_dto import TrashResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of TrashResponseDto from a JSON string
trash_response_dto_instance = TrashResponseDto.from_json(json)
# print the JSON string representation of the object
print(TrashResponseDto.to_json())

# convert the object into a dict
trash_response_dto_dict = trash_response_dto_instance.to_dict()
# create an instance of TrashResponseDto from a dict
trash_response_dto_from_dict = TrashResponseDto.from_dict(trash_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# PersonUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**birth_date** | **date** | Person date of birth | [optional] 
**color** | **str** | Person color (hex) | [optional] 
**feature_face_asset_id** | **UUID** | Asset ID used for feature face thumbnail | [optional] 
**is_favorite** | **bool** | Mark as favorite | [optional] 
**is_hidden** | **bool** | Person visibility (hidden) | [optional] 
**name** | **str** | Person name | [optional] 

## Example

```python
from immich_sdk.models.person_update_dto import PersonUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of PersonUpdateDto from a JSON string
person_update_dto_instance = PersonUpdateDto.from_json(json)
# print the JSON string representation of the object
print(PersonUpdateDto.to_json())

# convert the object into a dict
person_update_dto_dict = person_update_dto_instance.to_dict()
# create an instance of PersonUpdateDto from a dict
person_update_dto_from_dict = PersonUpdateDto.from_dict(person_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



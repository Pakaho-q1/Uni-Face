# PersonCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**birth_date** | **date** | Person date of birth | [optional] 
**color** | **str** | Person color (hex) | [optional] 
**is_favorite** | **bool** | Mark as favorite | [optional] 
**is_hidden** | **bool** | Person visibility (hidden) | [optional] 
**name** | **str** | Person name | [optional] 

## Example

```python
from immich_sdk.models.person_create_dto import PersonCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of PersonCreateDto from a JSON string
person_create_dto_instance = PersonCreateDto.from_json(json)
# print the JSON string representation of the object
print(PersonCreateDto.to_json())

# convert the object into a dict
person_create_dto_dict = person_create_dto_instance.to_dict()
# create an instance of PersonCreateDto from a dict
person_create_dto_from_dict = PersonCreateDto.from_dict(person_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



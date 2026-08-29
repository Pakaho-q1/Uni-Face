# PeopleUpdateItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**birth_date** | **date** | Person date of birth | [optional] 
**color** | **str** | Person color (hex) | [optional] 
**feature_face_asset_id** | **UUID** | Asset ID used for feature face thumbnail | [optional] 
**id** | **UUID** | Person ID | 
**is_favorite** | **bool** | Mark as favorite | [optional] 
**is_hidden** | **bool** | Person visibility (hidden) | [optional] 
**name** | **str** | Person name | [optional] 

## Example

```python
from immich_sdk.models.people_update_item import PeopleUpdateItem

# TODO update the JSON string below
json = "{}"
# create an instance of PeopleUpdateItem from a JSON string
people_update_item_instance = PeopleUpdateItem.from_json(json)
# print the JSON string representation of the object
print(PeopleUpdateItem.to_json())

# convert the object into a dict
people_update_item_dict = people_update_item_instance.to_dict()
# create an instance of PeopleUpdateItem from a dict
people_update_item_from_dict = PeopleUpdateItem.from_dict(people_update_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



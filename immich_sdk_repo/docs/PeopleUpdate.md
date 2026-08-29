# PeopleUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether people are enabled | [optional] 
**minimum_faces** | **int** | People face threshold | [optional] 
**sidebar_web** | **bool** | Whether people appear in web sidebar | [optional] 

## Example

```python
from immich_sdk.models.people_update import PeopleUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PeopleUpdate from a JSON string
people_update_instance = PeopleUpdate.from_json(json)
# print the JSON string representation of the object
print(PeopleUpdate.to_json())

# convert the object into a dict
people_update_dict = people_update_instance.to_dict()
# create an instance of PeopleUpdate from a dict
people_update_from_dict = PeopleUpdate.from_dict(people_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# SyncPersonV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**birth_date** | **datetime** | Birth date | 
**color** | **str** | Color | 
**created_at** | **datetime** | Created at | 
**face_asset_id** | **str** | Face asset ID | 
**id** | **UUID** | Person ID | 
**is_favorite** | **bool** | Is favorite | 
**is_hidden** | **bool** | Is hidden | 
**name** | **str** | Person name | 
**owner_id** | **UUID** | Owner ID | 
**updated_at** | **datetime** | Updated at | 

## Example

```python
from immich_sdk.models.sync_person_v1 import SyncPersonV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncPersonV1 from a JSON string
sync_person_v1_instance = SyncPersonV1.from_json(json)
# print the JSON string representation of the object
print(SyncPersonV1.to_json())

# convert the object into a dict
sync_person_v1_dict = sync_person_v1_instance.to_dict()
# create an instance of SyncPersonV1 from a dict
sync_person_v1_from_dict = SyncPersonV1.from_dict(sync_person_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



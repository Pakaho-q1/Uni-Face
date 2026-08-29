# SyncPartnerDeleteV1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_by_id** | **UUID** | Shared by ID | 
**shared_with_id** | **UUID** | Shared with ID | 

## Example

```python
from immich_sdk.models.sync_partner_delete_v1 import SyncPartnerDeleteV1

# TODO update the JSON string below
json = "{}"
# create an instance of SyncPartnerDeleteV1 from a JSON string
sync_partner_delete_v1_instance = SyncPartnerDeleteV1.from_json(json)
# print the JSON string representation of the object
print(SyncPartnerDeleteV1.to_json())

# convert the object into a dict
sync_partner_delete_v1_dict = sync_partner_delete_v1_instance.to_dict()
# create an instance of SyncPartnerDeleteV1 from a dict
sync_partner_delete_v1_from_dict = SyncPartnerDeleteV1.from_dict(sync_partner_delete_v1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



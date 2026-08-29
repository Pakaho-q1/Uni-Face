# MemoriesUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**duration** | **int** | Memory duration in seconds | [optional] 
**enabled** | **bool** | Whether memories are enabled | [optional] 
**sidebar_web** | **bool** | Whether memories appear in web sidebar | [optional] 

## Example

```python
from immich_sdk.models.memories_update import MemoriesUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of MemoriesUpdate from a JSON string
memories_update_instance = MemoriesUpdate.from_json(json)
# print the JSON string representation of the object
print(MemoriesUpdate.to_json())

# convert the object into a dict
memories_update_dict = memories_update_instance.to_dict()
# create an instance of MemoriesUpdate from a dict
memories_update_from_dict = MemoriesUpdate.from_dict(memories_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



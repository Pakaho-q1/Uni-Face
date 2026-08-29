# FoldersUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Whether folders are enabled | [optional] 
**sidebar_web** | **bool** | Whether folders appear in web sidebar | [optional] 

## Example

```python
from immich_sdk.models.folders_update import FoldersUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of FoldersUpdate from a JSON string
folders_update_instance = FoldersUpdate.from_json(json)
# print the JSON string representation of the object
print(FoldersUpdate.to_json())

# convert the object into a dict
folders_update_dict = folders_update_instance.to_dict()
# create an instance of FoldersUpdate from a dict
folders_update_from_dict = FoldersUpdate.from_dict(folders_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



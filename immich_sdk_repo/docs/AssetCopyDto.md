# AssetCopyDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**albums** | **bool** | Copy album associations | [optional] [default to True]
**favorite** | **bool** | Copy favorite status | [optional] [default to True]
**shared_links** | **bool** | Copy shared links | [optional] [default to True]
**sidecar** | **bool** | Copy sidecar file | [optional] [default to True]
**source_id** | **UUID** | Source asset ID | 
**stack** | **bool** | Copy stack association | [optional] [default to True]
**target_id** | **UUID** | Target asset ID | 

## Example

```python
from immich_sdk.models.asset_copy_dto import AssetCopyDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetCopyDto from a JSON string
asset_copy_dto_instance = AssetCopyDto.from_json(json)
# print the JSON string representation of the object
print(AssetCopyDto.to_json())

# convert the object into a dict
asset_copy_dto_dict = asset_copy_dto_instance.to_dict()
# create an instance of AssetCopyDto from a dict
asset_copy_dto_from_dict = AssetCopyDto.from_dict(asset_copy_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



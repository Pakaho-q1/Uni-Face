# AssetFaceDeleteDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**force** | **bool** | Force delete even if person has other faces | 

## Example

```python
from immich_sdk.models.asset_face_delete_dto import AssetFaceDeleteDto

# TODO update the JSON string below
json = "{}"
# create an instance of AssetFaceDeleteDto from a JSON string
asset_face_delete_dto_instance = AssetFaceDeleteDto.from_json(json)
# print the JSON string representation of the object
print(AssetFaceDeleteDto.to_json())

# convert the object into a dict
asset_face_delete_dto_dict = asset_face_delete_dto_instance.to_dict()
# create an instance of AssetFaceDeleteDto from a dict
asset_face_delete_dto_from_dict = AssetFaceDeleteDto.from_dict(asset_face_delete_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



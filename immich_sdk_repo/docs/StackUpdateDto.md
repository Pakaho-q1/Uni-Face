# StackUpdateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**primary_asset_id** | **UUID** | Primary asset ID | [optional] 

## Example

```python
from immich_sdk.models.stack_update_dto import StackUpdateDto

# TODO update the JSON string below
json = "{}"
# create an instance of StackUpdateDto from a JSON string
stack_update_dto_instance = StackUpdateDto.from_json(json)
# print the JSON string representation of the object
print(StackUpdateDto.to_json())

# convert the object into a dict
stack_update_dto_dict = stack_update_dto_instance.to_dict()
# create an instance of StackUpdateDto from a dict
stack_update_dto_from_dict = StackUpdateDto.from_dict(stack_update_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



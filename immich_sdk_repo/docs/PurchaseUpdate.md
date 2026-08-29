# PurchaseUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hide_buy_button_until** | **str** | Date until which to hide buy button | [optional] 
**show_support_badge** | **bool** | Whether to show support badge | [optional] 

## Example

```python
from immich_sdk.models.purchase_update import PurchaseUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseUpdate from a JSON string
purchase_update_instance = PurchaseUpdate.from_json(json)
# print the JSON string representation of the object
print(PurchaseUpdate.to_json())

# convert the object into a dict
purchase_update_dict = purchase_update_instance.to_dict()
# create an instance of PurchaseUpdate from a dict
purchase_update_from_dict = PurchaseUpdate.from_dict(purchase_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



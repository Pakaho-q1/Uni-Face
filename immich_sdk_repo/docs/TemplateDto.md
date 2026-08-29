# TemplateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**template** | **str** | Template name | 

## Example

```python
from immich_sdk.models.template_dto import TemplateDto

# TODO update the JSON string below
json = "{}"
# create an instance of TemplateDto from a JSON string
template_dto_instance = TemplateDto.from_json(json)
# print the JSON string representation of the object
print(TemplateDto.to_json())

# convert the object into a dict
template_dto_dict = template_dto_instance.to_dict()
# create an instance of TemplateDto from a dict
template_dto_from_dict = TemplateDto.from_dict(template_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# OnboardingDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_onboarded** | **bool** | Is user onboarded | 

## Example

```python
from immich_sdk.models.onboarding_dto import OnboardingDto

# TODO update the JSON string below
json = "{}"
# create an instance of OnboardingDto from a JSON string
onboarding_dto_instance = OnboardingDto.from_json(json)
# print the JSON string representation of the object
print(OnboardingDto.to_json())

# convert the object into a dict
onboarding_dto_dict = onboarding_dto_instance.to_dict()
# create an instance of OnboardingDto from a dict
onboarding_dto_from_dict = OnboardingDto.from_dict(onboarding_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



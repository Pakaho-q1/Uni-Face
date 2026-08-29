# OnboardingResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_onboarded** | **bool** | Is user onboarded | 

## Example

```python
from immich_sdk.models.onboarding_response_dto import OnboardingResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of OnboardingResponseDto from a JSON string
onboarding_response_dto_instance = OnboardingResponseDto.from_json(json)
# print the JSON string representation of the object
print(OnboardingResponseDto.to_json())

# convert the object into a dict
onboarding_response_dto_dict = onboarding_response_dto_instance.to_dict()
# create an instance of OnboardingResponseDto from a dict
onboarding_response_dto_from_dict = OnboardingResponseDto.from_dict(onboarding_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



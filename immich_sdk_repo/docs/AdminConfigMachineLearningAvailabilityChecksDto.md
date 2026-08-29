# AdminConfigMachineLearningAvailabilityChecksDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** | Enabled | 
**interval** | **int** |  | 
**timeout** | **int** |  | 

## Example

```python
from immich_sdk.models.admin_config_machine_learning_availability_checks_dto import AdminConfigMachineLearningAvailabilityChecksDto

# TODO update the JSON string below
json = "{}"
# create an instance of AdminConfigMachineLearningAvailabilityChecksDto from a JSON string
admin_config_machine_learning_availability_checks_dto_instance = AdminConfigMachineLearningAvailabilityChecksDto.from_json(json)
# print the JSON string representation of the object
print(AdminConfigMachineLearningAvailabilityChecksDto.to_json())

# convert the object into a dict
admin_config_machine_learning_availability_checks_dto_dict = admin_config_machine_learning_availability_checks_dto_instance.to_dict()
# create an instance of AdminConfigMachineLearningAvailabilityChecksDto from a dict
admin_config_machine_learning_availability_checks_dto_from_dict = AdminConfigMachineLearningAvailabilityChecksDto.from_dict(admin_config_machine_learning_availability_checks_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



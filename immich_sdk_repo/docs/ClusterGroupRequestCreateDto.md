# ClusterGroupRequestCreateDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **UUID** | User to invite into the cluster group | 

## Example

```python
from immich_sdk.models.cluster_group_request_create_dto import ClusterGroupRequestCreateDto

# TODO update the JSON string below
json = "{}"
# create an instance of ClusterGroupRequestCreateDto from a JSON string
cluster_group_request_create_dto_instance = ClusterGroupRequestCreateDto.from_json(json)
# print the JSON string representation of the object
print(ClusterGroupRequestCreateDto.to_json())

# convert the object into a dict
cluster_group_request_create_dto_dict = cluster_group_request_create_dto_instance.to_dict()
# create an instance of ClusterGroupRequestCreateDto from a dict
cluster_group_request_create_dto_from_dict = ClusterGroupRequestCreateDto.from_dict(cluster_group_request_create_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



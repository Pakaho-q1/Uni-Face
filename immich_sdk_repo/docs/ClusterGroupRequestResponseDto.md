# ClusterGroupRequestResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_group_id** | **UUID** | Cluster group the user is invited to join | 
**created_at** | **datetime** | Creation date | 
**id** | **UUID** | Request ID | 
**user_id** | **UUID** | User the request was created for | 

## Example

```python
from immich_sdk.models.cluster_group_request_response_dto import ClusterGroupRequestResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of ClusterGroupRequestResponseDto from a JSON string
cluster_group_request_response_dto_instance = ClusterGroupRequestResponseDto.from_json(json)
# print the JSON string representation of the object
print(ClusterGroupRequestResponseDto.to_json())

# convert the object into a dict
cluster_group_request_response_dto_dict = cluster_group_request_response_dto_instance.to_dict()
# create an instance of ClusterGroupRequestResponseDto from a dict
cluster_group_request_response_dto_from_dict = ClusterGroupRequestResponseDto.from_dict(cluster_group_request_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



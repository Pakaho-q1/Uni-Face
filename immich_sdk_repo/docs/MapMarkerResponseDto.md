# MapMarkerResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**city** | **str** | City name | 
**country** | **str** | Country name | 
**id** | **UUID** | Asset ID | 
**lat** | **float** | Latitude | 
**lon** | **float** | Longitude | 
**state** | **str** | State/Province name | 

## Example

```python
from immich_sdk.models.map_marker_response_dto import MapMarkerResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of MapMarkerResponseDto from a JSON string
map_marker_response_dto_instance = MapMarkerResponseDto.from_json(json)
# print the JSON string representation of the object
print(MapMarkerResponseDto.to_json())

# convert the object into a dict
map_marker_response_dto_dict = map_marker_response_dto_instance.to_dict()
# create an instance of MapMarkerResponseDto from a dict
map_marker_response_dto_from_dict = MapMarkerResponseDto.from_dict(map_marker_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



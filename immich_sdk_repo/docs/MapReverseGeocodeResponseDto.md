# MapReverseGeocodeResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**city** | **str** | City name | 
**country** | **str** | Country name | 
**state** | **str** | State/Province name | 

## Example

```python
from immich_sdk.models.map_reverse_geocode_response_dto import MapReverseGeocodeResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of MapReverseGeocodeResponseDto from a JSON string
map_reverse_geocode_response_dto_instance = MapReverseGeocodeResponseDto.from_json(json)
# print the JSON string representation of the object
print(MapReverseGeocodeResponseDto.to_json())

# convert the object into a dict
map_reverse_geocode_response_dto_dict = map_reverse_geocode_response_dto_instance.to_dict()
# create an instance of MapReverseGeocodeResponseDto from a dict
map_reverse_geocode_response_dto_from_dict = MapReverseGeocodeResponseDto.from_dict(map_reverse_geocode_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



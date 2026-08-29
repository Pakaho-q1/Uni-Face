# CalendarHeatmapResponseDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_from** | **str** | Start date in UTC | 
**series** | [**List[CalendarHeatmapResponseDtoSeriesInner]**](CalendarHeatmapResponseDtoSeriesInner.md) |  | 
**to** | **str** | End date in UTC | 
**total_count** | **int** | Total activity count over the period | 

## Example

```python
from immich_sdk.models.calendar_heatmap_response_dto import CalendarHeatmapResponseDto

# TODO update the JSON string below
json = "{}"
# create an instance of CalendarHeatmapResponseDto from a JSON string
calendar_heatmap_response_dto_instance = CalendarHeatmapResponseDto.from_json(json)
# print the JSON string representation of the object
print(CalendarHeatmapResponseDto.to_json())

# convert the object into a dict
calendar_heatmap_response_dto_dict = calendar_heatmap_response_dto_instance.to_dict()
# create an instance of CalendarHeatmapResponseDto from a dict
calendar_heatmap_response_dto_from_dict = CalendarHeatmapResponseDto.from_dict(calendar_heatmap_response_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



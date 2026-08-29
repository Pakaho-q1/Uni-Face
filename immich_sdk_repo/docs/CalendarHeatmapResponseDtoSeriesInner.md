# CalendarHeatmapResponseDtoSeriesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Activity count | 
**var_date** | **str** | Date in UTC | 

## Example

```python
from immich_sdk.models.calendar_heatmap_response_dto_series_inner import CalendarHeatmapResponseDtoSeriesInner

# TODO update the JSON string below
json = "{}"
# create an instance of CalendarHeatmapResponseDtoSeriesInner from a JSON string
calendar_heatmap_response_dto_series_inner_instance = CalendarHeatmapResponseDtoSeriesInner.from_json(json)
# print the JSON string representation of the object
print(CalendarHeatmapResponseDtoSeriesInner.to_json())

# convert the object into a dict
calendar_heatmap_response_dto_series_inner_dict = calendar_heatmap_response_dto_series_inner_instance.to_dict()
# create an instance of CalendarHeatmapResponseDtoSeriesInner from a dict
calendar_heatmap_response_dto_series_inner_from_dict = CalendarHeatmapResponseDtoSeriesInner.from_dict(calendar_heatmap_response_dto_series_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



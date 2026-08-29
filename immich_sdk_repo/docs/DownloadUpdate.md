# DownloadUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archive_size** | **int** | Maximum archive size in bytes | [optional] 
**include_embedded_videos** | **bool** | Whether to include embedded videos in downloads | [optional] 

## Example

```python
from immich_sdk.models.download_update import DownloadUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of DownloadUpdate from a JSON string
download_update_instance = DownloadUpdate.from_json(json)
# print the JSON string representation of the object
print(DownloadUpdate.to_json())

# convert the object into a dict
download_update_dict = download_update_instance.to_dict()
# create an instance of DownloadUpdate from a dict
download_update_from_dict = DownloadUpdate.from_dict(download_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



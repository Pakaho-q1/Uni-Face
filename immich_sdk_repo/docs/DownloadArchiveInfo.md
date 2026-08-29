# DownloadArchiveInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_ids** | **List[UUID]** | Asset IDs in this archive | 
**size** | **int** | Archive size in bytes | 

## Example

```python
from immich_sdk.models.download_archive_info import DownloadArchiveInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DownloadArchiveInfo from a JSON string
download_archive_info_instance = DownloadArchiveInfo.from_json(json)
# print the JSON string representation of the object
print(DownloadArchiveInfo.to_json())

# convert the object into a dict
download_archive_info_dict = download_archive_info_instance.to_dict()
# create an instance of DownloadArchiveInfo from a dict
download_archive_info_from_dict = DownloadArchiveInfo.from_dict(download_archive_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



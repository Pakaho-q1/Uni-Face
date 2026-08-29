# DownloadArchiveDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archive_name** | **str** | The name of the archive to download, without extension | [optional] 
**asset_ids** | **List[UUID]** | Asset IDs | 
**edited** | **bool** | Download edited asset if available | [optional] 

## Example

```python
from immich_sdk.models.download_archive_dto import DownloadArchiveDto

# TODO update the JSON string below
json = "{}"
# create an instance of DownloadArchiveDto from a JSON string
download_archive_dto_instance = DownloadArchiveDto.from_json(json)
# print the JSON string representation of the object
print(DownloadArchiveDto.to_json())

# convert the object into a dict
download_archive_dto_dict = download_archive_dto_instance.to_dict()
# create an instance of DownloadArchiveDto from a dict
download_archive_dto_from_dict = DownloadArchiveDto.from_dict(download_archive_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



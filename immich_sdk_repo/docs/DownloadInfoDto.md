# DownloadInfoDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**album_id** | **UUID** | Album ID to download | [optional] 
**archive_size** | **int** | Archive size limit in bytes | [optional] 
**asset_ids** | **List[UUID]** | Asset IDs to download | [optional] 
**user_id** | **UUID** | User ID to download assets from | [optional] 

## Example

```python
from immich_sdk.models.download_info_dto import DownloadInfoDto

# TODO update the JSON string below
json = "{}"
# create an instance of DownloadInfoDto from a JSON string
download_info_dto_instance = DownloadInfoDto.from_json(json)
# print the JSON string representation of the object
print(DownloadInfoDto.to_json())

# convert the object into a dict
download_info_dto_dict = download_info_dto_instance.to_dict()
# create an instance of DownloadInfoDto from a dict
download_info_dto_from_dict = DownloadInfoDto.from_dict(download_info_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



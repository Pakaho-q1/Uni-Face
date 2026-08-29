# immich_sdk.DownloadApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_archive**](DownloadApi.md#download_archive) | **POST** /download/archive | Download asset archive
[**get_download_info**](DownloadApi.md#get_download_info) | **POST** /download/info | Retrieve download information


# **download_archive**
> bytes download_archive(download_archive_dto, key=key, slug=slug)

Download asset archive

Download a ZIP archive containing the specified assets. The assets must have been previously requested via the "getDownloadInfo" endpoint.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.download_archive_dto import DownloadArchiveDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookie
configuration.api_key['cookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookie'] = 'Bearer'

# Configure API key authorization: api_key
configuration.api_key['api_key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Configure Bearer authorization (JWT): bearer
configuration = immich_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.DownloadApi(api_client)
    download_archive_dto = immich_sdk.DownloadArchiveDto() # DownloadArchiveDto | 
    key = 'key_example' # str |  (optional)
    slug = 'slug_example' # str |  (optional)

    try:
        # Download asset archive
        api_response = api_instance.download_archive(download_archive_dto, key=key, slug=slug)
        print("The response of DownloadApi->download_archive:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DownloadApi->download_archive: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **download_archive_dto** | [**DownloadArchiveDto**](DownloadArchiveDto.md)|  | 
 **key** | **str**|  | [optional] 
 **slug** | **str**|  | [optional] 

### Return type

**bytes**

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_download_info**
> DownloadResponseDto get_download_info(download_info_dto, key=key, slug=slug)

Retrieve download information

Retrieve information about how to request a download for the specified assets or album. The response includes groups of assets that can be downloaded together.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.download_info_dto import DownloadInfoDto
from immich_sdk.models.download_response_dto import DownloadResponseDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookie
configuration.api_key['cookie'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookie'] = 'Bearer'

# Configure API key authorization: api_key
configuration.api_key['api_key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Configure Bearer authorization (JWT): bearer
configuration = immich_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.DownloadApi(api_client)
    download_info_dto = immich_sdk.DownloadInfoDto() # DownloadInfoDto | 
    key = 'key_example' # str |  (optional)
    slug = 'slug_example' # str |  (optional)

    try:
        # Retrieve download information
        api_response = api_instance.get_download_info(download_info_dto, key=key, slug=slug)
        print("The response of DownloadApi->get_download_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DownloadApi->get_download_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **download_info_dto** | [**DownloadInfoDto**](DownloadInfoDto.md)|  | 
 **key** | **str**|  | [optional] 
 **slug** | **str**|  | [optional] 

### Return type

[**DownloadResponseDto**](DownloadResponseDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


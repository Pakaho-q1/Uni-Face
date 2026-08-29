# immich_sdk.ServerApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_server_license**](ServerApi.md#delete_server_license) | **DELETE** /server/license | Delete server product key
[**get_about_info**](ServerApi.md#get_about_info) | **GET** /server/about | Get server information
[**get_apk_links**](ServerApi.md#get_apk_links) | **GET** /server/apk-links | Get APK links
[**get_server_config**](ServerApi.md#get_server_config) | **GET** /server/config | Get config
[**get_server_features**](ServerApi.md#get_server_features) | **GET** /server/features | Get features
[**get_server_license**](ServerApi.md#get_server_license) | **GET** /server/license | Get product key
[**get_server_statistics**](ServerApi.md#get_server_statistics) | **GET** /server/statistics | Get statistics
[**get_server_version**](ServerApi.md#get_server_version) | **GET** /server/version | Get server version
[**get_storage**](ServerApi.md#get_storage) | **GET** /server/storage | Get storage
[**get_supported_media_types**](ServerApi.md#get_supported_media_types) | **GET** /server/media-types | Get supported media types
[**get_version_check**](ServerApi.md#get_version_check) | **GET** /server/version-check | Get version check status
[**get_version_history**](ServerApi.md#get_version_history) | **GET** /server/version-history | Get version history
[**ping_server**](ServerApi.md#ping_server) | **GET** /server/ping | Ping
[**set_server_license**](ServerApi.md#set_server_license) | **PUT** /server/license | Set server product key


# **delete_server_license**
> delete_server_license()

Delete server product key

Delete the currently set server product key.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Delete server product key
        api_instance.delete_server_license()
    except Exception as e:
        print("Exception when calling ServerApi->delete_server_license: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_about_info**
> ServerAboutResponseDto get_about_info()

Get server information

Retrieve a list of information about the server.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.server_about_response_dto import ServerAboutResponseDto
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get server information
        api_response = api_instance.get_about_info()
        print("The response of ServerApi->get_about_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_about_info: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerAboutResponseDto**](ServerAboutResponseDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_apk_links**
> ServerApkLinksDto get_apk_links()

Get APK links

Retrieve links to the APKs for the current server version.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.server_apk_links_dto import ServerApkLinksDto
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get APK links
        api_response = api_instance.get_apk_links()
        print("The response of ServerApi->get_apk_links:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_apk_links: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerApkLinksDto**](ServerApkLinksDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_server_config**
> ServerConfigDto get_server_config()

Get config

Retrieve the current server configuration.

### Example


```python
import immich_sdk
from immich_sdk.models.server_config_dto import ServerConfigDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get config
        api_response = api_instance.get_server_config()
        print("The response of ServerApi->get_server_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_server_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerConfigDto**](ServerConfigDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_server_features**
> ServerFeaturesDto get_server_features()

Get features

Retrieve available features supported by this server.

### Example


```python
import immich_sdk
from immich_sdk.models.server_features_dto import ServerFeaturesDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get features
        api_response = api_instance.get_server_features()
        print("The response of ServerApi->get_server_features:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_server_features: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerFeaturesDto**](ServerFeaturesDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_server_license**
> UserLicense get_server_license()

Get product key

Retrieve information about whether the server currently has a product key registered.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.user_license import UserLicense
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get product key
        api_response = api_instance.get_server_license()
        print("The response of ServerApi->get_server_license:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_server_license: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserLicense**](UserLicense.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_server_statistics**
> ServerStatsResponseDto get_server_statistics()

Get statistics

Retrieve statistics about the entire Immich instance such as asset counts.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.server_stats_response_dto import ServerStatsResponseDto
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get statistics
        api_response = api_instance.get_server_statistics()
        print("The response of ServerApi->get_server_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_server_statistics: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerStatsResponseDto**](ServerStatsResponseDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_server_version**
> ServerVersionResponseDto get_server_version()

Get server version

Retrieve the current server version in semantic versioning (semver) format.

### Example


```python
import immich_sdk
from immich_sdk.models.server_version_response_dto import ServerVersionResponseDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get server version
        api_response = api_instance.get_server_version()
        print("The response of ServerApi->get_server_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_server_version: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerVersionResponseDto**](ServerVersionResponseDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_storage**
> ServerStorageResponseDto get_storage()

Get storage

Retrieve the current storage utilization information of the server.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.server_storage_response_dto import ServerStorageResponseDto
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get storage
        api_response = api_instance.get_storage()
        print("The response of ServerApi->get_storage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_storage: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerStorageResponseDto**](ServerStorageResponseDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supported_media_types**
> ServerMediaTypesResponseDto get_supported_media_types()

Get supported media types

Retrieve all media types supported by the server.

### Example


```python
import immich_sdk
from immich_sdk.models.server_media_types_response_dto import ServerMediaTypesResponseDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get supported media types
        api_response = api_instance.get_supported_media_types()
        print("The response of ServerApi->get_supported_media_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_supported_media_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerMediaTypesResponseDto**](ServerMediaTypesResponseDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_version_check**
> VersionCheckStateResponseDto get_version_check()

Get version check status

Retrieve information about the last time the version check ran.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.version_check_state_response_dto import VersionCheckStateResponseDto
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
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get version check status
        api_response = api_instance.get_version_check()
        print("The response of ServerApi->get_version_check:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_version_check: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**VersionCheckStateResponseDto**](VersionCheckStateResponseDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_version_history**
> List[ServerVersionHistoryResponseDto] get_version_history()

Get version history

Retrieve a list of past versions the server has been on.

### Example


```python
import immich_sdk
from immich_sdk.models.server_version_history_response_dto import ServerVersionHistoryResponseDto
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Get version history
        api_response = api_instance.get_version_history()
        print("The response of ServerApi->get_version_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->get_version_history: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ServerVersionHistoryResponseDto]**](ServerVersionHistoryResponseDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ping_server**
> ServerPingResponse ping_server()

Ping

Pong

### Example


```python
import immich_sdk
from immich_sdk.models.server_ping_response import ServerPingResponse
from immich_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = immich_sdk.Configuration(
    host = "/api"
)


# Enter a context with an instance of the API client
with immich_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = immich_sdk.ServerApi(api_client)

    try:
        # Ping
        api_response = api_instance.ping_server()
        print("The response of ServerApi->ping_server:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->ping_server: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ServerPingResponse**](ServerPingResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_server_license**
> UserLicense set_server_license(license_key_dto)

Set server product key

Validate and set the server product key if successful.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.license_key_dto import LicenseKeyDto
from immich_sdk.models.user_license import UserLicense
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
    api_instance = immich_sdk.ServerApi(api_client)
    license_key_dto = immich_sdk.LicenseKeyDto() # LicenseKeyDto | 

    try:
        # Set server product key
        api_response = api_instance.set_server_license(license_key_dto)
        print("The response of ServerApi->set_server_license:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServerApi->set_server_license: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **license_key_dto** | [**LicenseKeyDto**](LicenseKeyDto.md)|  | 

### Return type

[**UserLicense**](UserLicense.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


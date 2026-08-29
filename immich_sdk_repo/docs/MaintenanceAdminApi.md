# immich_sdk.MaintenanceAdminApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_integrity_report**](MaintenanceAdminApi.md#delete_integrity_report) | **DELETE** /admin/integrity/report/{id} | Delete integrity report item
[**detect_prior_install**](MaintenanceAdminApi.md#detect_prior_install) | **GET** /admin/maintenance/detect-install | Detect existing install
[**get_integrity_report**](MaintenanceAdminApi.md#get_integrity_report) | **GET** /admin/integrity/report | Get integrity report by type
[**get_integrity_report_csv**](MaintenanceAdminApi.md#get_integrity_report_csv) | **GET** /admin/integrity/report/{type}/csv | Export integrity report by type as CSV
[**get_integrity_report_file**](MaintenanceAdminApi.md#get_integrity_report_file) | **GET** /admin/integrity/report/{id}/file | Download flagged file
[**get_integrity_report_summary**](MaintenanceAdminApi.md#get_integrity_report_summary) | **GET** /admin/integrity/summary | Get integrity report summary
[**get_maintenance_status**](MaintenanceAdminApi.md#get_maintenance_status) | **GET** /admin/maintenance/status | Get maintenance mode status
[**maintenance_login**](MaintenanceAdminApi.md#maintenance_login) | **POST** /admin/maintenance/login | Log into maintenance mode
[**set_maintenance_mode**](MaintenanceAdminApi.md#set_maintenance_mode) | **POST** /admin/maintenance | Set maintenance mode


# **delete_integrity_report**
> delete_integrity_report(id)

Delete integrity report item

Delete a given report item and perform corresponding deletion (e.g. trash asset, delete file)

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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Delete integrity report item
        api_instance.delete_integrity_report(id)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->delete_integrity_report: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

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
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detect_prior_install**
> MaintenanceDetectInstallResponseDto detect_prior_install()

Detect existing install

Collect integrity checks and other heuristics about local data.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.maintenance_detect_install_response_dto import MaintenanceDetectInstallResponseDto
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)

    try:
        # Detect existing install
        api_response = api_instance.detect_prior_install()
        print("The response of MaintenanceAdminApi->detect_prior_install:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->detect_prior_install: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**MaintenanceDetectInstallResponseDto**](MaintenanceDetectInstallResponseDto.md)

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

# **get_integrity_report**
> IntegrityReportResponseDto get_integrity_report(type, cursor=cursor, limit=limit)

Get integrity report by type

Get all flagged items by integrity report type

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.integrity_report import IntegrityReport
from immich_sdk.models.integrity_report_response_dto import IntegrityReportResponseDto
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)
    type = immich_sdk.IntegrityReport() # IntegrityReport | 
    cursor = 'cursor_example' # str | Cursor for pagination (optional)
    limit = 500 # int | Number of items per page (optional) (default to 500)

    try:
        # Get integrity report by type
        api_response = api_instance.get_integrity_report(type, cursor=cursor, limit=limit)
        print("The response of MaintenanceAdminApi->get_integrity_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->get_integrity_report: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | [**IntegrityReport**](.md)|  | 
 **cursor** | **str**| Cursor for pagination | [optional] 
 **limit** | **int**| Number of items per page | [optional] [default to 500]

### Return type

[**IntegrityReportResponseDto**](IntegrityReportResponseDto.md)

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

# **get_integrity_report_csv**
> bytes get_integrity_report_csv(type)

Export integrity report by type as CSV

Get all integrity report entries for a given type as a CSV

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.integrity_report import IntegrityReport
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)
    type = immich_sdk.IntegrityReport() # IntegrityReport | 

    try:
        # Export integrity report by type as CSV
        api_response = api_instance.get_integrity_report_csv(type)
        print("The response of MaintenanceAdminApi->get_integrity_report_csv:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->get_integrity_report_csv: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | [**IntegrityReport**](.md)|  | 

### Return type

**bytes**

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_integrity_report_file**
> bytes get_integrity_report_file(id)

Download flagged file

Download the untracked/broken file if one exists

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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Download flagged file
        api_response = api_instance.get_integrity_report_file(id)
        print("The response of MaintenanceAdminApi->get_integrity_report_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->get_integrity_report_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

**bytes**

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_integrity_report_summary**
> IntegrityReportSummaryResponseDto get_integrity_report_summary()

Get integrity report summary

Get a count of the items flagged in each integrity report

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.integrity_report_summary_response_dto import IntegrityReportSummaryResponseDto
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)

    try:
        # Get integrity report summary
        api_response = api_instance.get_integrity_report_summary()
        print("The response of MaintenanceAdminApi->get_integrity_report_summary:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->get_integrity_report_summary: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**IntegrityReportSummaryResponseDto**](IntegrityReportSummaryResponseDto.md)

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

# **get_maintenance_status**
> MaintenanceStatusResponseDto get_maintenance_status()

Get maintenance mode status

Fetch information about the currently running maintenance action.

### Example


```python
import immich_sdk
from immich_sdk.models.maintenance_status_response_dto import MaintenanceStatusResponseDto
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)

    try:
        # Get maintenance mode status
        api_response = api_instance.get_maintenance_status()
        print("The response of MaintenanceAdminApi->get_maintenance_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->get_maintenance_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**MaintenanceStatusResponseDto**](MaintenanceStatusResponseDto.md)

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

# **maintenance_login**
> MaintenanceAuthDto maintenance_login(maintenance_login_dto)

Log into maintenance mode

Login with maintenance token or cookie to receive current information and perform further actions.

### Example


```python
import immich_sdk
from immich_sdk.models.maintenance_auth_dto import MaintenanceAuthDto
from immich_sdk.models.maintenance_login_dto import MaintenanceLoginDto
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)
    maintenance_login_dto = immich_sdk.MaintenanceLoginDto() # MaintenanceLoginDto | 

    try:
        # Log into maintenance mode
        api_response = api_instance.maintenance_login(maintenance_login_dto)
        print("The response of MaintenanceAdminApi->maintenance_login:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->maintenance_login: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **maintenance_login_dto** | [**MaintenanceLoginDto**](MaintenanceLoginDto.md)|  | 

### Return type

[**MaintenanceAuthDto**](MaintenanceAuthDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_maintenance_mode**
> set_maintenance_mode(set_maintenance_mode_dto)

Set maintenance mode

Put Immich into or take it out of maintenance mode

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.set_maintenance_mode_dto import SetMaintenanceModeDto
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
    api_instance = immich_sdk.MaintenanceAdminApi(api_client)
    set_maintenance_mode_dto = immich_sdk.SetMaintenanceModeDto() # SetMaintenanceModeDto | 

    try:
        # Set maintenance mode
        api_instance.set_maintenance_mode(set_maintenance_mode_dto)
    except Exception as e:
        print("Exception when calling MaintenanceAdminApi->set_maintenance_mode: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **set_maintenance_mode_dto** | [**SetMaintenanceModeDto**](SetMaintenanceModeDto.md)|  | 

### Return type

void (empty response body)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


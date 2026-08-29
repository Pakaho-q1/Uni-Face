# immich_sdk.SystemMetadataApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_admin_onboarding**](SystemMetadataApi.md#get_admin_onboarding) | **GET** /system-metadata/admin-onboarding | Retrieve admin onboarding
[**get_reverse_geocoding_state**](SystemMetadataApi.md#get_reverse_geocoding_state) | **GET** /system-metadata/reverse-geocoding-state | Retrieve reverse geocoding state
[**get_version_check_state**](SystemMetadataApi.md#get_version_check_state) | **GET** /system-metadata/version-check-state | Retrieve version check state
[**update_admin_onboarding**](SystemMetadataApi.md#update_admin_onboarding) | **POST** /system-metadata/admin-onboarding | Update admin onboarding


# **get_admin_onboarding**
> AdminOnboardingUpdateDto get_admin_onboarding()

Retrieve admin onboarding

Retrieve the current admin onboarding status.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.admin_onboarding_update_dto import AdminOnboardingUpdateDto
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
    api_instance = immich_sdk.SystemMetadataApi(api_client)

    try:
        # Retrieve admin onboarding
        api_response = api_instance.get_admin_onboarding()
        print("The response of SystemMetadataApi->get_admin_onboarding:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemMetadataApi->get_admin_onboarding: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AdminOnboardingUpdateDto**](AdminOnboardingUpdateDto.md)

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

# **get_reverse_geocoding_state**
> ReverseGeocodingStateResponseDto get_reverse_geocoding_state()

Retrieve reverse geocoding state

Retrieve the current state of the reverse geocoding import.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.reverse_geocoding_state_response_dto import ReverseGeocodingStateResponseDto
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
    api_instance = immich_sdk.SystemMetadataApi(api_client)

    try:
        # Retrieve reverse geocoding state
        api_response = api_instance.get_reverse_geocoding_state()
        print("The response of SystemMetadataApi->get_reverse_geocoding_state:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemMetadataApi->get_reverse_geocoding_state: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ReverseGeocodingStateResponseDto**](ReverseGeocodingStateResponseDto.md)

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

# **get_version_check_state**
> VersionCheckStateResponseDto get_version_check_state()

Retrieve version check state

Retrieve the current state of the version check process.

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
    api_instance = immich_sdk.SystemMetadataApi(api_client)

    try:
        # Retrieve version check state
        api_response = api_instance.get_version_check_state()
        print("The response of SystemMetadataApi->get_version_check_state:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemMetadataApi->get_version_check_state: %s\n" % e)
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

# **update_admin_onboarding**
> update_admin_onboarding(admin_onboarding_update_dto)

Update admin onboarding

Update the admin onboarding status.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.admin_onboarding_update_dto import AdminOnboardingUpdateDto
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
    api_instance = immich_sdk.SystemMetadataApi(api_client)
    admin_onboarding_update_dto = immich_sdk.AdminOnboardingUpdateDto() # AdminOnboardingUpdateDto | 

    try:
        # Update admin onboarding
        api_instance.update_admin_onboarding(admin_onboarding_update_dto)
    except Exception as e:
        print("Exception when calling SystemMetadataApi->update_admin_onboarding: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **admin_onboarding_update_dto** | [**AdminOnboardingUpdateDto**](AdminOnboardingUpdateDto.md)|  | 

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
**204** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


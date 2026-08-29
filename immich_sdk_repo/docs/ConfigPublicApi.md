# immich_sdk.ConfigPublicApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_public_config**](ConfigPublicApi.md#get_public_config) | **GET** /public/config | Get the public configuration
[**get_public_config_defaults**](ConfigPublicApi.md#get_public_config_defaults) | **GET** /public/config/defaults | Get the public configuration defaults


# **get_public_config**
> PublicConfigDto get_public_config()

Get the public configuration

Retrieve the system configuration properties that are visible to everyone.

### Example


```python
import immich_sdk
from immich_sdk.models.public_config_dto import PublicConfigDto
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
    api_instance = immich_sdk.ConfigPublicApi(api_client)

    try:
        # Get the public configuration
        api_response = api_instance.get_public_config()
        print("The response of ConfigPublicApi->get_public_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigPublicApi->get_public_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PublicConfigDto**](PublicConfigDto.md)

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

# **get_public_config_defaults**
> PublicConfigDto get_public_config_defaults()

Get the public configuration defaults

Retrieve the default value of the configuration properties that are visible to everyone.

### Example


```python
import immich_sdk
from immich_sdk.models.public_config_dto import PublicConfigDto
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
    api_instance = immich_sdk.ConfigPublicApi(api_client)

    try:
        # Get the public configuration defaults
        api_response = api_instance.get_public_config_defaults()
        print("The response of ConfigPublicApi->get_public_config_defaults:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigPublicApi->get_public_config_defaults: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PublicConfigDto**](PublicConfigDto.md)

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


# immich_sdk.PluginsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_plugin**](PluginsApi.md#get_plugin) | **GET** /plugins/{id} | Retrieve a plugin
[**search_plugin_methods**](PluginsApi.md#search_plugin_methods) | **GET** /plugins/methods | Retrieve plugin methods
[**search_plugin_templates**](PluginsApi.md#search_plugin_templates) | **GET** /plugins/templates | Retrieve workflow templates
[**search_plugins**](PluginsApi.md#search_plugins) | **GET** /plugins | List all plugins


# **get_plugin**
> PluginResponseDto get_plugin(id)

Retrieve a plugin

Retrieve information about a specific plugin by its ID.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.plugin_response_dto import PluginResponseDto
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
    api_instance = immich_sdk.PluginsApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Retrieve a plugin
        api_response = api_instance.get_plugin(id)
        print("The response of PluginsApi->get_plugin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PluginsApi->get_plugin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**PluginResponseDto**](PluginResponseDto.md)

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

# **search_plugin_methods**
> List[PluginMethodResponseDto] search_plugin_methods(description=description, enabled=enabled, id=id, name=name, plugin_name=plugin_name, plugin_version=plugin_version, title=title, trigger=trigger, type=type)

Retrieve plugin methods

Retrieve a list of plugin methods

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.plugin_method_response_dto import PluginMethodResponseDto
from immich_sdk.models.workflow_trigger import WorkflowTrigger
from immich_sdk.models.workflow_type import WorkflowType
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
    api_instance = immich_sdk.PluginsApi(api_client)
    description = 'description_example' # str |  (optional)
    enabled = True # bool | Whether the plugin method is enabled (optional)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Plugin method ID (optional)
    name = 'name_example' # str |  (optional)
    plugin_name = 'plugin_name_example' # str | Plugin name (optional)
    plugin_version = 'plugin_version_example' # str | Plugin version (optional)
    title = 'title_example' # str |  (optional)
    trigger = immich_sdk.WorkflowTrigger() # WorkflowTrigger | Workflow trigger (optional)
    type = immich_sdk.WorkflowType() # WorkflowType | Workflow types (optional)

    try:
        # Retrieve plugin methods
        api_response = api_instance.search_plugin_methods(description=description, enabled=enabled, id=id, name=name, plugin_name=plugin_name, plugin_version=plugin_version, title=title, trigger=trigger, type=type)
        print("The response of PluginsApi->search_plugin_methods:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PluginsApi->search_plugin_methods: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **description** | **str**|  | [optional] 
 **enabled** | **bool**| Whether the plugin method is enabled | [optional] 
 **id** | **UUID**| Plugin method ID | [optional] 
 **name** | **str**|  | [optional] 
 **plugin_name** | **str**| Plugin name | [optional] 
 **plugin_version** | **str**| Plugin version | [optional] 
 **title** | **str**|  | [optional] 
 **trigger** | [**WorkflowTrigger**](.md)| Workflow trigger | [optional] 
 **type** | [**WorkflowType**](.md)| Workflow types | [optional] 

### Return type

[**List[PluginMethodResponseDto]**](PluginMethodResponseDto.md)

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

# **search_plugin_templates**
> List[PluginTemplateResponseDto] search_plugin_templates()

Retrieve workflow templates

Retrieve workflow templates provided by installed plugins

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.plugin_template_response_dto import PluginTemplateResponseDto
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
    api_instance = immich_sdk.PluginsApi(api_client)

    try:
        # Retrieve workflow templates
        api_response = api_instance.search_plugin_templates()
        print("The response of PluginsApi->search_plugin_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PluginsApi->search_plugin_templates: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PluginTemplateResponseDto]**](PluginTemplateResponseDto.md)

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

# **search_plugins**
> List[PluginResponseDto] search_plugins(description=description, enabled=enabled, id=id, name=name, title=title, version=version)

List all plugins

Retrieve a list of plugins available to the authenticated user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.plugin_response_dto import PluginResponseDto
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
    api_instance = immich_sdk.PluginsApi(api_client)
    description = 'description_example' # str |  (optional)
    enabled = True # bool | Whether the plugin is enabled (optional)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Plugin ID (optional)
    name = 'name_example' # str |  (optional)
    title = 'title_example' # str |  (optional)
    version = 'version_example' # str |  (optional)

    try:
        # List all plugins
        api_response = api_instance.search_plugins(description=description, enabled=enabled, id=id, name=name, title=title, version=version)
        print("The response of PluginsApi->search_plugins:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PluginsApi->search_plugins: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **description** | **str**|  | [optional] 
 **enabled** | **bool**| Whether the plugin is enabled | [optional] 
 **id** | **UUID**| Plugin ID | [optional] 
 **name** | **str**|  | [optional] 
 **title** | **str**|  | [optional] 
 **version** | **str**|  | [optional] 

### Return type

[**List[PluginResponseDto]**](PluginResponseDto.md)

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


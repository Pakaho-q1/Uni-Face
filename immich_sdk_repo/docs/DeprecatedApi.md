# immich_sdk.DeprecatedApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_partner_deprecated**](DeprecatedApi.md#create_partner_deprecated) | **POST** /partners/{id} | Create a partner
[**get_config**](DeprecatedApi.md#get_config) | **GET** /system-config | Get system configuration
[**get_config_defaults**](DeprecatedApi.md#get_config_defaults) | **GET** /system-config/defaults | Get system configuration defaults
[**get_queues_legacy**](DeprecatedApi.md#get_queues_legacy) | **GET** /jobs | Retrieve queue counts and status
[**get_server_config**](DeprecatedApi.md#get_server_config) | **GET** /server/config | Get config
[**get_server_features**](DeprecatedApi.md#get_server_features) | **GET** /server/features | Get features
[**run_queue_command_legacy**](DeprecatedApi.md#run_queue_command_legacy) | **PUT** /jobs/{name} | Run jobs
[**search_large_assets**](DeprecatedApi.md#search_large_assets) | **POST** /search/large-assets | Search large assets
[**update_api_key**](DeprecatedApi.md#update_api_key) | **PUT** /api-keys/{id} | Update an API key
[**update_asset**](DeprecatedApi.md#update_asset) | **PUT** /assets/{id} | Update an asset
[**update_assets**](DeprecatedApi.md#update_assets) | **PUT** /assets | Update assets
[**update_config**](DeprecatedApi.md#update_config) | **PUT** /system-config | Update system configuration
[**update_library**](DeprecatedApi.md#update_library) | **PUT** /libraries/{id} | Update a library
[**update_memory**](DeprecatedApi.md#update_memory) | **PUT** /memories/{id} | Update a memory
[**update_my_preferences**](DeprecatedApi.md#update_my_preferences) | **PUT** /users/me/preferences | Update my preferences
[**update_my_user**](DeprecatedApi.md#update_my_user) | **PUT** /users/me | Update current user
[**update_person**](DeprecatedApi.md#update_person) | **PUT** /people/{id} | Update person
[**update_session**](DeprecatedApi.md#update_session) | **PUT** /sessions/{id} | Update a session
[**update_stack**](DeprecatedApi.md#update_stack) | **PUT** /stacks/{id} | Update a stack
[**update_tag**](DeprecatedApi.md#update_tag) | **PUT** /tags/{id} | Update a tag
[**update_user_admin**](DeprecatedApi.md#update_user_admin) | **PUT** /admin/users/{id} | Update a user
[**update_user_preferences_admin**](DeprecatedApi.md#update_user_preferences_admin) | **PUT** /admin/users/{id}/preferences | Update user preferences
[**update_workflow**](DeprecatedApi.md#update_workflow) | **PUT** /workflows/{id} | Update a workflow


# **create_partner_deprecated**
> PartnerResponseDto create_partner_deprecated(id)

Create a partner

Create a new partner to share assets with.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.partner_response_dto import PartnerResponseDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Create a partner
        api_response = api_instance.create_partner_deprecated(id)
        print("The response of DeprecatedApi->create_partner_deprecated:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->create_partner_deprecated: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**PartnerResponseDto**](PartnerResponseDto.md)

### Authorization

[cookie](../README.md#cookie), [api_key](../README.md#api_key), [bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_config**
> AdminConfigDto get_config()

Get system configuration

Retrieve the current system configuration.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.admin_config_dto import AdminConfigDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)

    try:
        # Get system configuration
        api_response = api_instance.get_config()
        print("The response of DeprecatedApi->get_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->get_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AdminConfigDto**](AdminConfigDto.md)

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

# **get_config_defaults**
> AdminConfigDto get_config_defaults()

Get system configuration defaults

Retrieve the default values for the system configuration.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.admin_config_dto import AdminConfigDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)

    try:
        # Get system configuration defaults
        api_response = api_instance.get_config_defaults()
        print("The response of DeprecatedApi->get_config_defaults:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->get_config_defaults: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AdminConfigDto**](AdminConfigDto.md)

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

# **get_queues_legacy**
> QueuesResponseLegacyDto get_queues_legacy()

Retrieve queue counts and status

Retrieve the counts of the current queue, as well as the current status.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.queues_response_legacy_dto import QueuesResponseLegacyDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)

    try:
        # Retrieve queue counts and status
        api_response = api_instance.get_queues_legacy()
        print("The response of DeprecatedApi->get_queues_legacy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->get_queues_legacy: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**QueuesResponseLegacyDto**](QueuesResponseLegacyDto.md)

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
    api_instance = immich_sdk.DeprecatedApi(api_client)

    try:
        # Get config
        api_response = api_instance.get_server_config()
        print("The response of DeprecatedApi->get_server_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->get_server_config: %s\n" % e)
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
    api_instance = immich_sdk.DeprecatedApi(api_client)

    try:
        # Get features
        api_response = api_instance.get_server_features()
        print("The response of DeprecatedApi->get_server_features:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->get_server_features: %s\n" % e)
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

# **run_queue_command_legacy**
> QueueResponseLegacyDto run_queue_command_legacy(name, queue_command_dto)

Run jobs

Queue all assets for a specific job type. Defaults to only queueing assets that have not yet been processed, but the force command can be used to re-process all assets.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.queue_command_dto import QueueCommandDto
from immich_sdk.models.queue_name import QueueName
from immich_sdk.models.queue_response_legacy_dto import QueueResponseLegacyDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    name = immich_sdk.QueueName() # QueueName | 
    queue_command_dto = immich_sdk.QueueCommandDto() # QueueCommandDto | 

    try:
        # Run jobs
        api_response = api_instance.run_queue_command_legacy(name, queue_command_dto)
        print("The response of DeprecatedApi->run_queue_command_legacy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->run_queue_command_legacy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | [**QueueName**](.md)|  | 
 **queue_command_dto** | [**QueueCommandDto**](QueueCommandDto.md)|  | 

### Return type

[**QueueResponseLegacyDto**](QueueResponseLegacyDto.md)

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

# **search_large_assets**
> List[AssetResponseDto] search_large_assets(album_ids=album_ids, city=city, country=country, created_after=created_after, created_before=created_before, is_encoded=is_encoded, is_favorite=is_favorite, is_motion=is_motion, is_not_in_album=is_not_in_album, is_offline=is_offline, lens_model=lens_model, library_id=library_id, make=make, min_file_size=min_file_size, model=model, ocr=ocr, person_ids=person_ids, rating=rating, size=size, state=state, tag_ids=tag_ids, taken_after=taken_after, taken_before=taken_before, trashed_after=trashed_after, trashed_before=trashed_before, type=type, updated_after=updated_after, updated_before=updated_before, visibility=visibility, with_deleted=with_deleted, with_exif=with_exif)

Search large assets

Search for assets that are considered large based on specified criteria.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_response_dto import AssetResponseDto
from immich_sdk.models.asset_type_enum import AssetTypeEnum
from immich_sdk.models.asset_visibility import AssetVisibility
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    album_ids = None # List[UUID] | Filter by album IDs (optional)
    city = 'city_example' # str | Filter by city name (optional)
    country = 'country_example' # str | Filter by country name (optional)
    created_after = '2024-01-01T00:00Z' # datetime | Filter by creation date (after) (optional)
    created_before = '2024-01-01T00:00Z' # datetime | Filter by creation date (before) (optional)
    is_encoded = True # bool | Filter by encoded status (optional)
    is_favorite = True # bool | Filter by favorite status (optional)
    is_motion = True # bool | Filter by motion photo status (optional)
    is_not_in_album = True # bool | Filter assets not in any album (optional)
    is_offline = True # bool | Filter by offline status (optional)
    lens_model = 'lens_model_example' # str | Filter by lens model (optional)
    library_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Library ID to filter by (optional)
    make = 'make_example' # str | Filter by camera make (optional)
    min_file_size = 56 # int | Minimum file size in bytes (optional)
    model = 'model_example' # str | Filter by camera model (optional)
    ocr = 'ocr_example' # str | Filter by OCR text content (optional)
    person_ids = None # List[UUID] | Filter by person IDs (optional)
    rating = 56 # int | Filter by rating [1-5], or null for unrated (optional)
    size = 250 # int | Number of results to return (optional) (default to 250)
    state = 'state_example' # str | Filter by state/province name (optional)
    tag_ids = None # List[UUID] | Filter by tag IDs (optional)
    taken_after = '2024-01-01T00:00Z' # datetime | Filter by taken date (after) (optional)
    taken_before = '2024-01-01T00:00Z' # datetime | Filter by taken date (before) (optional)
    trashed_after = '2024-01-01T00:00Z' # datetime | Filter by trash date (after) (optional)
    trashed_before = '2024-01-01T00:00Z' # datetime | Filter by trash date (before) (optional)
    type = immich_sdk.AssetTypeEnum() # AssetTypeEnum |  (optional)
    updated_after = '2024-01-01T00:00Z' # datetime | Filter by update date (after) (optional)
    updated_before = '2024-01-01T00:00Z' # datetime | Filter by update date (before) (optional)
    visibility = immich_sdk.AssetVisibility() # AssetVisibility |  (optional)
    with_deleted = True # bool | Include deleted assets (optional)
    with_exif = True # bool | Include EXIF data in response (optional)

    try:
        # Search large assets
        api_response = api_instance.search_large_assets(album_ids=album_ids, city=city, country=country, created_after=created_after, created_before=created_before, is_encoded=is_encoded, is_favorite=is_favorite, is_motion=is_motion, is_not_in_album=is_not_in_album, is_offline=is_offline, lens_model=lens_model, library_id=library_id, make=make, min_file_size=min_file_size, model=model, ocr=ocr, person_ids=person_ids, rating=rating, size=size, state=state, tag_ids=tag_ids, taken_after=taken_after, taken_before=taken_before, trashed_after=trashed_after, trashed_before=trashed_before, type=type, updated_after=updated_after, updated_before=updated_before, visibility=visibility, with_deleted=with_deleted, with_exif=with_exif)
        print("The response of DeprecatedApi->search_large_assets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->search_large_assets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **album_ids** | [**List[UUID]**](UUID.md)| Filter by album IDs | [optional] 
 **city** | **str**| Filter by city name | [optional] 
 **country** | **str**| Filter by country name | [optional] 
 **created_after** | **datetime**| Filter by creation date (after) | [optional] 
 **created_before** | **datetime**| Filter by creation date (before) | [optional] 
 **is_encoded** | **bool**| Filter by encoded status | [optional] 
 **is_favorite** | **bool**| Filter by favorite status | [optional] 
 **is_motion** | **bool**| Filter by motion photo status | [optional] 
 **is_not_in_album** | **bool**| Filter assets not in any album | [optional] 
 **is_offline** | **bool**| Filter by offline status | [optional] 
 **lens_model** | **str**| Filter by lens model | [optional] 
 **library_id** | **UUID**| Library ID to filter by | [optional] 
 **make** | **str**| Filter by camera make | [optional] 
 **min_file_size** | **int**| Minimum file size in bytes | [optional] 
 **model** | **str**| Filter by camera model | [optional] 
 **ocr** | **str**| Filter by OCR text content | [optional] 
 **person_ids** | [**List[UUID]**](UUID.md)| Filter by person IDs | [optional] 
 **rating** | **int**| Filter by rating [1-5], or null for unrated | [optional] 
 **size** | **int**| Number of results to return | [optional] [default to 250]
 **state** | **str**| Filter by state/province name | [optional] 
 **tag_ids** | [**List[UUID]**](UUID.md)| Filter by tag IDs | [optional] 
 **taken_after** | **datetime**| Filter by taken date (after) | [optional] 
 **taken_before** | **datetime**| Filter by taken date (before) | [optional] 
 **trashed_after** | **datetime**| Filter by trash date (after) | [optional] 
 **trashed_before** | **datetime**| Filter by trash date (before) | [optional] 
 **type** | [**AssetTypeEnum**](.md)|  | [optional] 
 **updated_after** | **datetime**| Filter by update date (after) | [optional] 
 **updated_before** | **datetime**| Filter by update date (before) | [optional] 
 **visibility** | [**AssetVisibility**](.md)|  | [optional] 
 **with_deleted** | **bool**| Include deleted assets | [optional] 
 **with_exif** | **bool**| Include EXIF data in response | [optional] 

### Return type

[**List[AssetResponseDto]**](AssetResponseDto.md)

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

# **update_api_key**
> ApiKeyResponseDto update_api_key(id, api_key_update_dto)

Update an API key

Updates the name and permissions of an API key by its ID. The current user must own this API key.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.api_key_response_dto import ApiKeyResponseDto
from immich_sdk.models.api_key_update_dto import ApiKeyUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    api_key_update_dto = immich_sdk.ApiKeyUpdateDto() # ApiKeyUpdateDto | 

    try:
        # Update an API key
        api_response = api_instance.update_api_key(id, api_key_update_dto)
        print("The response of DeprecatedApi->update_api_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_api_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **api_key_update_dto** | [**ApiKeyUpdateDto**](ApiKeyUpdateDto.md)|  | 

### Return type

[**ApiKeyResponseDto**](ApiKeyResponseDto.md)

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

# **update_asset**
> AssetResponseDto update_asset(id, update_asset_dto)

Update an asset

Update information of a specific asset.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_response_dto import AssetResponseDto
from immich_sdk.models.update_asset_dto import UpdateAssetDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    update_asset_dto = immich_sdk.UpdateAssetDto() # UpdateAssetDto | 

    try:
        # Update an asset
        api_response = api_instance.update_asset(id, update_asset_dto)
        print("The response of DeprecatedApi->update_asset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_asset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **update_asset_dto** | [**UpdateAssetDto**](UpdateAssetDto.md)|  | 

### Return type

[**AssetResponseDto**](AssetResponseDto.md)

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

# **update_assets**
> update_assets(asset_bulk_update_dto)

Update assets

Updates multiple assets at the same time.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_bulk_update_dto import AssetBulkUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    asset_bulk_update_dto = immich_sdk.AssetBulkUpdateDto() # AssetBulkUpdateDto | 

    try:
        # Update assets
        api_instance.update_assets(asset_bulk_update_dto)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_assets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_bulk_update_dto** | [**AssetBulkUpdateDto**](AssetBulkUpdateDto.md)|  | 

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

# **update_config**
> AdminConfigDto update_config(admin_config_dto)

Update system configuration

Update the system configuration with a new system configuration.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.admin_config_dto import AdminConfigDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    admin_config_dto = immich_sdk.AdminConfigDto() # AdminConfigDto | 

    try:
        # Update system configuration
        api_response = api_instance.update_config(admin_config_dto)
        print("The response of DeprecatedApi->update_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **admin_config_dto** | [**AdminConfigDto**](AdminConfigDto.md)|  | 

### Return type

[**AdminConfigDto**](AdminConfigDto.md)

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

# **update_library**
> LibraryResponseDto update_library(id, update_library_dto)

Update a library

Update an existing external library.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.library_response_dto import LibraryResponseDto
from immich_sdk.models.update_library_dto import UpdateLibraryDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    update_library_dto = immich_sdk.UpdateLibraryDto() # UpdateLibraryDto | 

    try:
        # Update a library
        api_response = api_instance.update_library(id, update_library_dto)
        print("The response of DeprecatedApi->update_library:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_library: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **update_library_dto** | [**UpdateLibraryDto**](UpdateLibraryDto.md)|  | 

### Return type

[**LibraryResponseDto**](LibraryResponseDto.md)

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

# **update_memory**
> MemoryResponseDto update_memory(id, memory_update_dto)

Update a memory

Update an existing memory by its ID.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.memory_response_dto import MemoryResponseDto
from immich_sdk.models.memory_update_dto import MemoryUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    memory_update_dto = immich_sdk.MemoryUpdateDto() # MemoryUpdateDto | 

    try:
        # Update a memory
        api_response = api_instance.update_memory(id, memory_update_dto)
        print("The response of DeprecatedApi->update_memory:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_memory: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **memory_update_dto** | [**MemoryUpdateDto**](MemoryUpdateDto.md)|  | 

### Return type

[**MemoryResponseDto**](MemoryResponseDto.md)

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

# **update_my_preferences**
> UserPreferencesResponseDto update_my_preferences(user_preferences_update_dto)

Update my preferences

Update the preferences of the current user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.user_preferences_response_dto import UserPreferencesResponseDto
from immich_sdk.models.user_preferences_update_dto import UserPreferencesUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    user_preferences_update_dto = immich_sdk.UserPreferencesUpdateDto() # UserPreferencesUpdateDto | 

    try:
        # Update my preferences
        api_response = api_instance.update_my_preferences(user_preferences_update_dto)
        print("The response of DeprecatedApi->update_my_preferences:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_my_preferences: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_preferences_update_dto** | [**UserPreferencesUpdateDto**](UserPreferencesUpdateDto.md)|  | 

### Return type

[**UserPreferencesResponseDto**](UserPreferencesResponseDto.md)

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

# **update_my_user**
> UserAdminResponseDto update_my_user(user_update_me_dto)

Update current user

Update the current user making the API request.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto
from immich_sdk.models.user_update_me_dto import UserUpdateMeDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    user_update_me_dto = immich_sdk.UserUpdateMeDto() # UserUpdateMeDto | 

    try:
        # Update current user
        api_response = api_instance.update_my_user(user_update_me_dto)
        print("The response of DeprecatedApi->update_my_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_my_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_update_me_dto** | [**UserUpdateMeDto**](UserUpdateMeDto.md)|  | 

### Return type

[**UserAdminResponseDto**](UserAdminResponseDto.md)

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

# **update_person**
> PersonResponseDto update_person(id, person_update_dto)

Update person

Update an individual person.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.person_response_dto import PersonResponseDto
from immich_sdk.models.person_update_dto import PersonUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    person_update_dto = immich_sdk.PersonUpdateDto() # PersonUpdateDto | 

    try:
        # Update person
        api_response = api_instance.update_person(id, person_update_dto)
        print("The response of DeprecatedApi->update_person:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_person: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **person_update_dto** | [**PersonUpdateDto**](PersonUpdateDto.md)|  | 

### Return type

[**PersonResponseDto**](PersonResponseDto.md)

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

# **update_session**
> SessionResponseDto update_session(id, session_update_dto)

Update a session

Update a specific session identified by id.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.session_response_dto import SessionResponseDto
from immich_sdk.models.session_update_dto import SessionUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    session_update_dto = immich_sdk.SessionUpdateDto() # SessionUpdateDto | 

    try:
        # Update a session
        api_response = api_instance.update_session(id, session_update_dto)
        print("The response of DeprecatedApi->update_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **session_update_dto** | [**SessionUpdateDto**](SessionUpdateDto.md)|  | 

### Return type

[**SessionResponseDto**](SessionResponseDto.md)

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

# **update_stack**
> StackResponseDto update_stack(id, stack_update_dto)

Update a stack

Update an existing stack by its ID.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.stack_response_dto import StackResponseDto
from immich_sdk.models.stack_update_dto import StackUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    stack_update_dto = immich_sdk.StackUpdateDto() # StackUpdateDto | 

    try:
        # Update a stack
        api_response = api_instance.update_stack(id, stack_update_dto)
        print("The response of DeprecatedApi->update_stack:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_stack: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **stack_update_dto** | [**StackUpdateDto**](StackUpdateDto.md)|  | 

### Return type

[**StackResponseDto**](StackResponseDto.md)

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

# **update_tag**
> TagResponseDto update_tag(id, tag_update_dto)

Update a tag

Update an existing tag identified by its ID.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.tag_response_dto import TagResponseDto
from immich_sdk.models.tag_update_dto import TagUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    tag_update_dto = immich_sdk.TagUpdateDto() # TagUpdateDto | 

    try:
        # Update a tag
        api_response = api_instance.update_tag(id, tag_update_dto)
        print("The response of DeprecatedApi->update_tag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_tag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **tag_update_dto** | [**TagUpdateDto**](TagUpdateDto.md)|  | 

### Return type

[**TagResponseDto**](TagResponseDto.md)

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

# **update_user_admin**
> UserAdminResponseDto update_user_admin(id, user_admin_update_dto)

Update a user

Update an existing user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto
from immich_sdk.models.user_admin_update_dto import UserAdminUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    user_admin_update_dto = immich_sdk.UserAdminUpdateDto() # UserAdminUpdateDto | 

    try:
        # Update a user
        api_response = api_instance.update_user_admin(id, user_admin_update_dto)
        print("The response of DeprecatedApi->update_user_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_user_admin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **user_admin_update_dto** | [**UserAdminUpdateDto**](UserAdminUpdateDto.md)|  | 

### Return type

[**UserAdminResponseDto**](UserAdminResponseDto.md)

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

# **update_user_preferences_admin**
> UserPreferencesResponseDto update_user_preferences_admin(id, user_preferences_update_dto)

Update user preferences

Update the preferences of a specific user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.user_preferences_response_dto import UserPreferencesResponseDto
from immich_sdk.models.user_preferences_update_dto import UserPreferencesUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    user_preferences_update_dto = immich_sdk.UserPreferencesUpdateDto() # UserPreferencesUpdateDto | 

    try:
        # Update user preferences
        api_response = api_instance.update_user_preferences_admin(id, user_preferences_update_dto)
        print("The response of DeprecatedApi->update_user_preferences_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_user_preferences_admin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **user_preferences_update_dto** | [**UserPreferencesUpdateDto**](UserPreferencesUpdateDto.md)|  | 

### Return type

[**UserPreferencesResponseDto**](UserPreferencesResponseDto.md)

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

# **update_workflow**
> WorkflowResponseDto update_workflow(id, workflow_update_dto)

Update a workflow

Update the information of a specific workflow by its ID. This endpoint can be used to update the workflow name, description, trigger type, filters and actions order, etc.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.workflow_response_dto import WorkflowResponseDto
from immich_sdk.models.workflow_update_dto import WorkflowUpdateDto
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
    api_instance = immich_sdk.DeprecatedApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    workflow_update_dto = immich_sdk.WorkflowUpdateDto() # WorkflowUpdateDto | 

    try:
        # Update a workflow
        api_response = api_instance.update_workflow(id, workflow_update_dto)
        print("The response of DeprecatedApi->update_workflow:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DeprecatedApi->update_workflow: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **workflow_update_dto** | [**WorkflowUpdateDto**](WorkflowUpdateDto.md)|  | 

### Return type

[**WorkflowResponseDto**](WorkflowResponseDto.md)

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


# immich_sdk.MemoriesApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_memory_assets**](MemoriesApi.md#add_memory_assets) | **PUT** /memories/{id}/assets | Add assets to a memory
[**create_memory**](MemoriesApi.md#create_memory) | **POST** /memories | Create a memory
[**delete_memory**](MemoriesApi.md#delete_memory) | **DELETE** /memories/{id} | Delete a memory
[**get_memory**](MemoriesApi.md#get_memory) | **GET** /memories/{id} | Retrieve a memory
[**memories_statistics**](MemoriesApi.md#memories_statistics) | **GET** /memories/statistics | Retrieve memories statistics
[**remove_memory_assets**](MemoriesApi.md#remove_memory_assets) | **DELETE** /memories/{id}/assets | Remove assets from a memory
[**search_memories**](MemoriesApi.md#search_memories) | **GET** /memories | Retrieve memories
[**update_memory**](MemoriesApi.md#update_memory) | **PUT** /memories/{id} | Update a memory


# **add_memory_assets**
> List[BulkIdResponseDto] add_memory_assets(id, bulk_ids_dto)

Add assets to a memory

Add a list of asset IDs to a specific memory.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.bulk_id_response_dto import BulkIdResponseDto
from immich_sdk.models.bulk_ids_dto import BulkIdsDto
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
    api_instance = immich_sdk.MemoriesApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    bulk_ids_dto = immich_sdk.BulkIdsDto() # BulkIdsDto | 

    try:
        # Add assets to a memory
        api_response = api_instance.add_memory_assets(id, bulk_ids_dto)
        print("The response of MemoriesApi->add_memory_assets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->add_memory_assets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **bulk_ids_dto** | [**BulkIdsDto**](BulkIdsDto.md)|  | 

### Return type

[**List[BulkIdResponseDto]**](BulkIdResponseDto.md)

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

# **create_memory**
> MemoryResponseDto create_memory(memory_create_dto)

Create a memory

Create a new memory by providing a name, description, and a list of asset IDs to include in the memory.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.memory_create_dto import MemoryCreateDto
from immich_sdk.models.memory_response_dto import MemoryResponseDto
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
    api_instance = immich_sdk.MemoriesApi(api_client)
    memory_create_dto = immich_sdk.MemoryCreateDto() # MemoryCreateDto | 

    try:
        # Create a memory
        api_response = api_instance.create_memory(memory_create_dto)
        print("The response of MemoriesApi->create_memory:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->create_memory: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **memory_create_dto** | [**MemoryCreateDto**](MemoryCreateDto.md)|  | 

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
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_memory**
> delete_memory(id)

Delete a memory

Delete a specific memory by its ID.

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
    api_instance = immich_sdk.MemoriesApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Delete a memory
        api_instance.delete_memory(id)
    except Exception as e:
        print("Exception when calling MemoriesApi->delete_memory: %s\n" % e)
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
**204** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_memory**
> MemoryResponseDto get_memory(id)

Retrieve a memory

Retrieve a specific memory by its ID.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.memory_response_dto import MemoryResponseDto
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
    api_instance = immich_sdk.MemoriesApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Retrieve a memory
        api_response = api_instance.get_memory(id)
        print("The response of MemoriesApi->get_memory:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->get_memory: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**MemoryResponseDto**](MemoryResponseDto.md)

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

# **memories_statistics**
> MemoryStatisticsResponseDto memories_statistics(var_for=var_for, id=id, is_saved=is_saved, is_trashed=is_trashed, is_upcoming=is_upcoming, order=order, page=page, size=size, type=type)

Retrieve memories statistics

Retrieve statistics about memories, such as total count and other relevant metrics.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.memory_search_order import MemorySearchOrder
from immich_sdk.models.memory_statistics_response_dto import MemoryStatisticsResponseDto
from immich_sdk.models.memory_type import MemoryType
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
    api_instance = immich_sdk.MemoriesApi(api_client)
    var_for = 'Mon Jan 01 07:00:00 ICT 1481' # date | Filter by date (optional)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Memory ID (optional)
    is_saved = True # bool | Filter by saved status (optional)
    is_trashed = True # bool | Include trashed memories (optional)
    is_upcoming = True # bool | Filter by memories that have not been shown yet (optional)
    order = immich_sdk.MemorySearchOrder() # MemorySearchOrder |  (optional)
    page = 56 # int | Page number (optional)
    size = 56 # int | Number of memories to return (optional)
    type = immich_sdk.MemoryType() # MemoryType |  (optional)

    try:
        # Retrieve memories statistics
        api_response = api_instance.memories_statistics(var_for=var_for, id=id, is_saved=is_saved, is_trashed=is_trashed, is_upcoming=is_upcoming, order=order, page=page, size=size, type=type)
        print("The response of MemoriesApi->memories_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->memories_statistics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **var_for** | **date**| Filter by date | [optional] 
 **id** | **UUID**| Memory ID | [optional] 
 **is_saved** | **bool**| Filter by saved status | [optional] 
 **is_trashed** | **bool**| Include trashed memories | [optional] 
 **is_upcoming** | **bool**| Filter by memories that have not been shown yet | [optional] 
 **order** | [**MemorySearchOrder**](.md)|  | [optional] 
 **page** | **int**| Page number | [optional] 
 **size** | **int**| Number of memories to return | [optional] 
 **type** | [**MemoryType**](.md)|  | [optional] 

### Return type

[**MemoryStatisticsResponseDto**](MemoryStatisticsResponseDto.md)

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

# **remove_memory_assets**
> List[BulkIdResponseDto] remove_memory_assets(id, bulk_ids_dto)

Remove assets from a memory

Remove a list of asset IDs from a specific memory.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.bulk_id_response_dto import BulkIdResponseDto
from immich_sdk.models.bulk_ids_dto import BulkIdsDto
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
    api_instance = immich_sdk.MemoriesApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    bulk_ids_dto = immich_sdk.BulkIdsDto() # BulkIdsDto | 

    try:
        # Remove assets from a memory
        api_response = api_instance.remove_memory_assets(id, bulk_ids_dto)
        print("The response of MemoriesApi->remove_memory_assets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->remove_memory_assets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **bulk_ids_dto** | [**BulkIdsDto**](BulkIdsDto.md)|  | 

### Return type

[**List[BulkIdResponseDto]**](BulkIdResponseDto.md)

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

# **search_memories**
> List[MemoryResponseDto] search_memories(var_for=var_for, id=id, is_saved=is_saved, is_trashed=is_trashed, is_upcoming=is_upcoming, order=order, page=page, size=size, type=type)

Retrieve memories

Retrieve a list of memories. Memories are sorted descending by creation date by default, although they can also be sorted in ascending order, or randomly.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.memory_response_dto import MemoryResponseDto
from immich_sdk.models.memory_search_order import MemorySearchOrder
from immich_sdk.models.memory_type import MemoryType
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
    api_instance = immich_sdk.MemoriesApi(api_client)
    var_for = 'Mon Jan 01 07:00:00 ICT 1481' # date | Filter by date (optional)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Memory ID (optional)
    is_saved = True # bool | Filter by saved status (optional)
    is_trashed = True # bool | Include trashed memories (optional)
    is_upcoming = True # bool | Filter by memories that have not been shown yet (optional)
    order = immich_sdk.MemorySearchOrder() # MemorySearchOrder |  (optional)
    page = 56 # int | Page number (optional)
    size = 56 # int | Number of memories to return (optional)
    type = immich_sdk.MemoryType() # MemoryType |  (optional)

    try:
        # Retrieve memories
        api_response = api_instance.search_memories(var_for=var_for, id=id, is_saved=is_saved, is_trashed=is_trashed, is_upcoming=is_upcoming, order=order, page=page, size=size, type=type)
        print("The response of MemoriesApi->search_memories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->search_memories: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **var_for** | **date**| Filter by date | [optional] 
 **id** | **UUID**| Memory ID | [optional] 
 **is_saved** | **bool**| Filter by saved status | [optional] 
 **is_trashed** | **bool**| Include trashed memories | [optional] 
 **is_upcoming** | **bool**| Filter by memories that have not been shown yet | [optional] 
 **order** | [**MemorySearchOrder**](.md)|  | [optional] 
 **page** | **int**| Page number | [optional] 
 **size** | **int**| Number of memories to return | [optional] 
 **type** | [**MemoryType**](.md)|  | [optional] 

### Return type

[**List[MemoryResponseDto]**](MemoryResponseDto.md)

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
    api_instance = immich_sdk.MemoriesApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    memory_update_dto = immich_sdk.MemoryUpdateDto() # MemoryUpdateDto | 

    try:
        # Update a memory
        api_response = api_instance.update_memory(id, memory_update_dto)
        print("The response of MemoriesApi->update_memory:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemoriesApi->update_memory: %s\n" % e)
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


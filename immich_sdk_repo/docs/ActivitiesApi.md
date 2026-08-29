# immich_sdk.ActivitiesApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_activity**](ActivitiesApi.md#create_activity) | **POST** /activities | Create an activity
[**delete_activity**](ActivitiesApi.md#delete_activity) | **DELETE** /activities/{id} | Delete an activity
[**get_activities**](ActivitiesApi.md#get_activities) | **GET** /activities | List all activities
[**get_activity_statistics**](ActivitiesApi.md#get_activity_statistics) | **GET** /activities/statistics | Retrieve activity statistics


# **create_activity**
> ActivityResponseDto create_activity(activity_create_dto)

Create an activity

Create a like or a comment for an album, or an asset in an album.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.activity_create_dto import ActivityCreateDto
from immich_sdk.models.activity_response_dto import ActivityResponseDto
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
    api_instance = immich_sdk.ActivitiesApi(api_client)
    activity_create_dto = immich_sdk.ActivityCreateDto() # ActivityCreateDto | 

    try:
        # Create an activity
        api_response = api_instance.create_activity(activity_create_dto)
        print("The response of ActivitiesApi->create_activity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivitiesApi->create_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **activity_create_dto** | [**ActivityCreateDto**](ActivityCreateDto.md)|  | 

### Return type

[**ActivityResponseDto**](ActivityResponseDto.md)

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

# **delete_activity**
> delete_activity(id)

Delete an activity

Removes a like or comment from a given album or asset in an album.

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
    api_instance = immich_sdk.ActivitiesApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Delete an activity
        api_instance.delete_activity(id)
    except Exception as e:
        print("Exception when calling ActivitiesApi->delete_activity: %s\n" % e)
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

# **get_activities**
> List[ActivityResponseDto] get_activities(album_id, asset_id=asset_id, level=level, type=type, user_id=user_id)

List all activities

Returns a list of activities for the selected asset or album. The activities are returned in sorted order, with the oldest activities appearing first.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.activity_response_dto import ActivityResponseDto
from immich_sdk.models.reaction_level import ReactionLevel
from immich_sdk.models.reaction_type import ReactionType
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
    api_instance = immich_sdk.ActivitiesApi(api_client)
    album_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Album ID
    asset_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Asset ID (if activity is for an asset) (optional)
    level = immich_sdk.ReactionLevel() # ReactionLevel |  (optional)
    type = immich_sdk.ReactionType() # ReactionType |  (optional)
    user_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter by user ID (optional)

    try:
        # List all activities
        api_response = api_instance.get_activities(album_id, asset_id=asset_id, level=level, type=type, user_id=user_id)
        print("The response of ActivitiesApi->get_activities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivitiesApi->get_activities: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **album_id** | **UUID**| Album ID | 
 **asset_id** | **UUID**| Asset ID (if activity is for an asset) | [optional] 
 **level** | [**ReactionLevel**](.md)|  | [optional] 
 **type** | [**ReactionType**](.md)|  | [optional] 
 **user_id** | **UUID**| Filter by user ID | [optional] 

### Return type

[**List[ActivityResponseDto]**](ActivityResponseDto.md)

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

# **get_activity_statistics**
> ActivityStatisticsResponseDto get_activity_statistics(album_id, asset_id=asset_id)

Retrieve activity statistics

Returns the number of likes and comments for a given album or asset in an album.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.activity_statistics_response_dto import ActivityStatisticsResponseDto
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
    api_instance = immich_sdk.ActivitiesApi(api_client)
    album_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Album ID
    asset_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Asset ID (if activity is for an asset) (optional)

    try:
        # Retrieve activity statistics
        api_response = api_instance.get_activity_statistics(album_id, asset_id=asset_id)
        print("The response of ActivitiesApi->get_activity_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ActivitiesApi->get_activity_statistics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **album_id** | **UUID**| Album ID | 
 **asset_id** | **UUID**| Asset ID (if activity is for an asset) | [optional] 

### Return type

[**ActivityStatisticsResponseDto**](ActivityStatisticsResponseDto.md)

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


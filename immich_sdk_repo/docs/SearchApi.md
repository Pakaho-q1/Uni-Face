# immich_sdk.SearchApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_assets_by_city**](SearchApi.md#get_assets_by_city) | **GET** /search/cities | Retrieve assets by city
[**get_explore_data**](SearchApi.md#get_explore_data) | **GET** /search/explore | Retrieve explore data
[**get_search_suggestions**](SearchApi.md#get_search_suggestions) | **GET** /search/suggestions | Retrieve search suggestions
[**search_asset_statistics**](SearchApi.md#search_asset_statistics) | **POST** /search/statistics | Search asset statistics
[**search_assets**](SearchApi.md#search_assets) | **POST** /search/metadata | Search assets by metadata
[**search_large_assets**](SearchApi.md#search_large_assets) | **POST** /search/large-assets | Search large assets
[**search_person**](SearchApi.md#search_person) | **GET** /search/person | Search people
[**search_places**](SearchApi.md#search_places) | **GET** /search/places | Search places
[**search_random**](SearchApi.md#search_random) | **POST** /search/random | Search random assets
[**search_smart**](SearchApi.md#search_smart) | **POST** /search/smart | Smart asset search


# **get_assets_by_city**
> List[AssetResponseDto] get_assets_by_city()

Retrieve assets by city

Retrieve a list of assets with each asset belonging to a different city. This endpoint is used on the places pages to show a single thumbnail for each city the user has assets in.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_response_dto import AssetResponseDto
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
    api_instance = immich_sdk.SearchApi(api_client)

    try:
        # Retrieve assets by city
        api_response = api_instance.get_assets_by_city()
        print("The response of SearchApi->get_assets_by_city:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->get_assets_by_city: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

# **get_explore_data**
> List[SearchExploreResponseDto] get_explore_data()

Retrieve explore data

Retrieve data for the explore section, such as popular people and places.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.search_explore_response_dto import SearchExploreResponseDto
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
    api_instance = immich_sdk.SearchApi(api_client)

    try:
        # Retrieve explore data
        api_response = api_instance.get_explore_data()
        print("The response of SearchApi->get_explore_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->get_explore_data: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[SearchExploreResponseDto]**](SearchExploreResponseDto.md)

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

# **get_search_suggestions**
> List[str] get_search_suggestions(type, country=country, include_null=include_null, lens_model=lens_model, make=make, model=model, state=state)

Retrieve search suggestions

Retrieve search suggestions based on partial input. This endpoint is used for typeahead search features.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.search_suggestion_type import SearchSuggestionType
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
    api_instance = immich_sdk.SearchApi(api_client)
    type = immich_sdk.SearchSuggestionType() # SearchSuggestionType | 
    country = 'country_example' # str | Filter by country (optional)
    include_null = True # bool | Include null values in suggestions (optional)
    lens_model = 'lens_model_example' # str | Filter by lens model (optional)
    make = 'make_example' # str | Filter by camera make (optional)
    model = 'model_example' # str | Filter by camera model (optional)
    state = 'state_example' # str | Filter by state/province (optional)

    try:
        # Retrieve search suggestions
        api_response = api_instance.get_search_suggestions(type, country=country, include_null=include_null, lens_model=lens_model, make=make, model=model, state=state)
        print("The response of SearchApi->get_search_suggestions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->get_search_suggestions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | [**SearchSuggestionType**](.md)|  | 
 **country** | **str**| Filter by country | [optional] 
 **include_null** | **bool**| Include null values in suggestions | [optional] 
 **lens_model** | **str**| Filter by lens model | [optional] 
 **make** | **str**| Filter by camera make | [optional] 
 **model** | **str**| Filter by camera model | [optional] 
 **state** | **str**| Filter by state/province | [optional] 

### Return type

**List[str]**

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

# **search_asset_statistics**
> SearchStatisticsResponseDto search_asset_statistics(statistics_search_dto)

Search asset statistics

Retrieve statistical data about assets based on search criteria, such as the total matching count.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.search_statistics_response_dto import SearchStatisticsResponseDto
from immich_sdk.models.statistics_search_dto import StatisticsSearchDto
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
    api_instance = immich_sdk.SearchApi(api_client)
    statistics_search_dto = immich_sdk.StatisticsSearchDto() # StatisticsSearchDto | 

    try:
        # Search asset statistics
        api_response = api_instance.search_asset_statistics(statistics_search_dto)
        print("The response of SearchApi->search_asset_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_asset_statistics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **statistics_search_dto** | [**StatisticsSearchDto**](StatisticsSearchDto.md)|  | 

### Return type

[**SearchStatisticsResponseDto**](SearchStatisticsResponseDto.md)

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

# **search_assets**
> SearchResponseDto search_assets(metadata_search_dto, key=key, slug=slug)

Search assets by metadata

Search for assets based on various metadata criteria.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.metadata_search_dto import MetadataSearchDto
from immich_sdk.models.search_response_dto import SearchResponseDto
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
    api_instance = immich_sdk.SearchApi(api_client)
    metadata_search_dto = immich_sdk.MetadataSearchDto() # MetadataSearchDto | 
    key = 'key_example' # str |  (optional)
    slug = 'slug_example' # str |  (optional)

    try:
        # Search assets by metadata
        api_response = api_instance.search_assets(metadata_search_dto, key=key, slug=slug)
        print("The response of SearchApi->search_assets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_assets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metadata_search_dto** | [**MetadataSearchDto**](MetadataSearchDto.md)|  | 
 **key** | **str**|  | [optional] 
 **slug** | **str**|  | [optional] 

### Return type

[**SearchResponseDto**](SearchResponseDto.md)

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
    api_instance = immich_sdk.SearchApi(api_client)
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
        print("The response of SearchApi->search_large_assets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_large_assets: %s\n" % e)
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

# **search_person**
> List[PersonResponseDto] search_person(name, with_hidden=with_hidden)

Search people

Search for people by name.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.person_response_dto import PersonResponseDto
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
    api_instance = immich_sdk.SearchApi(api_client)
    name = 'name_example' # str | Person name to search for
    with_hidden = True # bool | Include hidden people (optional)

    try:
        # Search people
        api_response = api_instance.search_person(name, with_hidden=with_hidden)
        print("The response of SearchApi->search_person:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_person: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Person name to search for | 
 **with_hidden** | **bool**| Include hidden people | [optional] 

### Return type

[**List[PersonResponseDto]**](PersonResponseDto.md)

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

# **search_places**
> List[PlacesResponseDto] search_places(name)

Search places

Search for places by name.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.places_response_dto import PlacesResponseDto
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
    api_instance = immich_sdk.SearchApi(api_client)
    name = 'name_example' # str | Place name to search for

    try:
        # Search places
        api_response = api_instance.search_places(name)
        print("The response of SearchApi->search_places:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_places: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Place name to search for | 

### Return type

[**List[PlacesResponseDto]**](PlacesResponseDto.md)

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

# **search_random**
> List[AssetResponseDto] search_random(random_search_dto)

Search random assets

Retrieve a random selection of assets based on the provided criteria.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_response_dto import AssetResponseDto
from immich_sdk.models.random_search_dto import RandomSearchDto
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
    api_instance = immich_sdk.SearchApi(api_client)
    random_search_dto = immich_sdk.RandomSearchDto() # RandomSearchDto | 

    try:
        # Search random assets
        api_response = api_instance.search_random(random_search_dto)
        print("The response of SearchApi->search_random:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_random: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **random_search_dto** | [**RandomSearchDto**](RandomSearchDto.md)|  | 

### Return type

[**List[AssetResponseDto]**](AssetResponseDto.md)

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

# **search_smart**
> SearchResponseDto search_smart(smart_search_dto)

Smart asset search

Perform a smart search for assets by using machine learning vectors to determine relevance.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.search_response_dto import SearchResponseDto
from immich_sdk.models.smart_search_dto import SmartSearchDto
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
    api_instance = immich_sdk.SearchApi(api_client)
    smart_search_dto = immich_sdk.SmartSearchDto() # SmartSearchDto | 

    try:
        # Smart asset search
        api_response = api_instance.search_smart(smart_search_dto)
        print("The response of SearchApi->search_smart:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_smart: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **smart_search_dto** | [**SmartSearchDto**](SmartSearchDto.md)|  | 

### Return type

[**SearchResponseDto**](SearchResponseDto.md)

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


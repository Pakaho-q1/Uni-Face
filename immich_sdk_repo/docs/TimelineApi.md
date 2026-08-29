# immich_sdk.TimelineApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_time_bucket**](TimelineApi.md#get_time_bucket) | **GET** /timeline/bucket | Get time bucket
[**get_time_buckets**](TimelineApi.md#get_time_buckets) | **GET** /timeline/buckets | Get time buckets


# **get_time_bucket**
> TimeBucketAssetResponseDto get_time_bucket(time_bucket, album_id=album_id, bbox=bbox, is_favorite=is_favorite, is_trashed=is_trashed, key=key, order=order, order_by=order_by, person_id=person_id, slug=slug, tag_id=tag_id, user_id=user_id, visibility=visibility, with_coordinates=with_coordinates, with_partners=with_partners, with_stacked=with_stacked)

Get time bucket

Retrieve a string of all asset ids in a given time bucket.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_order import AssetOrder
from immich_sdk.models.asset_order_by import AssetOrderBy
from immich_sdk.models.asset_visibility import AssetVisibility
from immich_sdk.models.time_bucket_asset_response_dto import TimeBucketAssetResponseDto
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
    api_instance = immich_sdk.TimelineApi(api_client)
    time_bucket = '2024-01-01' # str | Time bucket identifier in YYYY-MM-DD format
    album_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets belonging to a specific album (optional)
    bbox = '11.075683,49.416711,11.117589,49.454875' # str | Bounding box coordinates as west,south,east,north (WGS84) (optional)
    is_favorite = True # bool | Filter by favorite status (true for favorites only, false for non-favorites only) (optional)
    is_trashed = True # bool | Filter by trash status (true for trashed assets only, false for non-trashed only) (optional)
    key = 'key_example' # str |  (optional)
    order = immich_sdk.AssetOrder() # AssetOrder | Sort order for assets within time buckets (ASC for oldest first, DESC for newest first) (optional)
    order_by = immich_sdk.AssetOrderBy() # AssetOrderBy | Date to group and order assets by (takenAt for date taken, createdAt for date added to Immich) (optional)
    person_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets containing a specific person (face recognition) (optional)
    slug = 'slug_example' # str |  (optional)
    tag_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets with a specific tag (optional)
    user_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets by specific user ID (optional)
    visibility = immich_sdk.AssetVisibility() # AssetVisibility | Filter by asset visibility status (ARCHIVE, TIMELINE, HIDDEN, LOCKED) (optional)
    with_coordinates = True # bool | Include location data in the response (optional)
    with_partners = True # bool | Include assets shared by partners (optional)
    with_stacked = True # bool | Include stacked assets in the response. When true, only primary assets from stacks are returned. (optional)

    try:
        # Get time bucket
        api_response = api_instance.get_time_bucket(time_bucket, album_id=album_id, bbox=bbox, is_favorite=is_favorite, is_trashed=is_trashed, key=key, order=order, order_by=order_by, person_id=person_id, slug=slug, tag_id=tag_id, user_id=user_id, visibility=visibility, with_coordinates=with_coordinates, with_partners=with_partners, with_stacked=with_stacked)
        print("The response of TimelineApi->get_time_bucket:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TimelineApi->get_time_bucket: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **time_bucket** | **str**| Time bucket identifier in YYYY-MM-DD format | 
 **album_id** | **UUID**| Filter assets belonging to a specific album | [optional] 
 **bbox** | **str**| Bounding box coordinates as west,south,east,north (WGS84) | [optional] 
 **is_favorite** | **bool**| Filter by favorite status (true for favorites only, false for non-favorites only) | [optional] 
 **is_trashed** | **bool**| Filter by trash status (true for trashed assets only, false for non-trashed only) | [optional] 
 **key** | **str**|  | [optional] 
 **order** | [**AssetOrder**](.md)| Sort order for assets within time buckets (ASC for oldest first, DESC for newest first) | [optional] 
 **order_by** | [**AssetOrderBy**](.md)| Date to group and order assets by (takenAt for date taken, createdAt for date added to Immich) | [optional] 
 **person_id** | **UUID**| Filter assets containing a specific person (face recognition) | [optional] 
 **slug** | **str**|  | [optional] 
 **tag_id** | **UUID**| Filter assets with a specific tag | [optional] 
 **user_id** | **UUID**| Filter assets by specific user ID | [optional] 
 **visibility** | [**AssetVisibility**](.md)| Filter by asset visibility status (ARCHIVE, TIMELINE, HIDDEN, LOCKED) | [optional] 
 **with_coordinates** | **bool**| Include location data in the response | [optional] 
 **with_partners** | **bool**| Include assets shared by partners | [optional] 
 **with_stacked** | **bool**| Include stacked assets in the response. When true, only primary assets from stacks are returned. | [optional] 

### Return type

[**TimeBucketAssetResponseDto**](TimeBucketAssetResponseDto.md)

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

# **get_time_buckets**
> List[TimeBucketsResponseDto] get_time_buckets(album_id=album_id, bbox=bbox, is_favorite=is_favorite, is_trashed=is_trashed, key=key, order=order, order_by=order_by, person_id=person_id, slug=slug, tag_id=tag_id, user_id=user_id, visibility=visibility, with_coordinates=with_coordinates, with_partners=with_partners, with_stacked=with_stacked)

Get time buckets

Retrieve a list of all minimal time buckets.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.asset_order import AssetOrder
from immich_sdk.models.asset_order_by import AssetOrderBy
from immich_sdk.models.asset_visibility import AssetVisibility
from immich_sdk.models.time_buckets_response_dto import TimeBucketsResponseDto
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
    api_instance = immich_sdk.TimelineApi(api_client)
    album_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets belonging to a specific album (optional)
    bbox = '11.075683,49.416711,11.117589,49.454875' # str | Bounding box coordinates as west,south,east,north (WGS84) (optional)
    is_favorite = True # bool | Filter by favorite status (true for favorites only, false for non-favorites only) (optional)
    is_trashed = True # bool | Filter by trash status (true for trashed assets only, false for non-trashed only) (optional)
    key = 'key_example' # str |  (optional)
    order = immich_sdk.AssetOrder() # AssetOrder | Sort order for assets within time buckets (ASC for oldest first, DESC for newest first) (optional)
    order_by = immich_sdk.AssetOrderBy() # AssetOrderBy | Date to group and order assets by (takenAt for date taken, createdAt for date added to Immich) (optional)
    person_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets containing a specific person (face recognition) (optional)
    slug = 'slug_example' # str |  (optional)
    tag_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets with a specific tag (optional)
    user_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter assets by specific user ID (optional)
    visibility = immich_sdk.AssetVisibility() # AssetVisibility | Filter by asset visibility status (ARCHIVE, TIMELINE, HIDDEN, LOCKED) (optional)
    with_coordinates = True # bool | Include location data in the response (optional)
    with_partners = True # bool | Include assets shared by partners (optional)
    with_stacked = True # bool | Include stacked assets in the response. When true, only primary assets from stacks are returned. (optional)

    try:
        # Get time buckets
        api_response = api_instance.get_time_buckets(album_id=album_id, bbox=bbox, is_favorite=is_favorite, is_trashed=is_trashed, key=key, order=order, order_by=order_by, person_id=person_id, slug=slug, tag_id=tag_id, user_id=user_id, visibility=visibility, with_coordinates=with_coordinates, with_partners=with_partners, with_stacked=with_stacked)
        print("The response of TimelineApi->get_time_buckets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TimelineApi->get_time_buckets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **album_id** | **UUID**| Filter assets belonging to a specific album | [optional] 
 **bbox** | **str**| Bounding box coordinates as west,south,east,north (WGS84) | [optional] 
 **is_favorite** | **bool**| Filter by favorite status (true for favorites only, false for non-favorites only) | [optional] 
 **is_trashed** | **bool**| Filter by trash status (true for trashed assets only, false for non-trashed only) | [optional] 
 **key** | **str**|  | [optional] 
 **order** | [**AssetOrder**](.md)| Sort order for assets within time buckets (ASC for oldest first, DESC for newest first) | [optional] 
 **order_by** | [**AssetOrderBy**](.md)| Date to group and order assets by (takenAt for date taken, createdAt for date added to Immich) | [optional] 
 **person_id** | **UUID**| Filter assets containing a specific person (face recognition) | [optional] 
 **slug** | **str**|  | [optional] 
 **tag_id** | **UUID**| Filter assets with a specific tag | [optional] 
 **user_id** | **UUID**| Filter assets by specific user ID | [optional] 
 **visibility** | [**AssetVisibility**](.md)| Filter by asset visibility status (ARCHIVE, TIMELINE, HIDDEN, LOCKED) | [optional] 
 **with_coordinates** | **bool**| Include location data in the response | [optional] 
 **with_partners** | **bool**| Include assets shared by partners | [optional] 
 **with_stacked** | **bool**| Include stacked assets in the response. When true, only primary assets from stacks are returned. | [optional] 

### Return type

[**List[TimeBucketsResponseDto]**](TimeBucketsResponseDto.md)

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


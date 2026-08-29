# immich_sdk.NotificationsAdminApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_notification**](NotificationsAdminApi.md#create_notification) | **POST** /admin/notifications | Create a notification
[**get_notification_template_admin**](NotificationsAdminApi.md#get_notification_template_admin) | **POST** /admin/notifications/templates/{name} | Render email template
[**send_test_email_admin**](NotificationsAdminApi.md#send_test_email_admin) | **POST** /admin/notifications/test-email | Send test email


# **create_notification**
> NotificationDto create_notification(notification_create_dto)

Create a notification

Create a new notification for a specific user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.notification_create_dto import NotificationCreateDto
from immich_sdk.models.notification_dto import NotificationDto
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
    api_instance = immich_sdk.NotificationsAdminApi(api_client)
    notification_create_dto = immich_sdk.NotificationCreateDto() # NotificationCreateDto | 

    try:
        # Create a notification
        api_response = api_instance.create_notification(notification_create_dto)
        print("The response of NotificationsAdminApi->create_notification:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationsAdminApi->create_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_create_dto** | [**NotificationCreateDto**](NotificationCreateDto.md)|  | 

### Return type

[**NotificationDto**](NotificationDto.md)

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

# **get_notification_template_admin**
> TemplateResponseDto get_notification_template_admin(name, template_dto)

Render email template

Retrieve a preview of the provided email template.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.template_dto import TemplateDto
from immich_sdk.models.template_response_dto import TemplateResponseDto
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
    api_instance = immich_sdk.NotificationsAdminApi(api_client)
    name = 'name_example' # str | 
    template_dto = immich_sdk.TemplateDto() # TemplateDto | 

    try:
        # Render email template
        api_response = api_instance.get_notification_template_admin(name, template_dto)
        print("The response of NotificationsAdminApi->get_notification_template_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationsAdminApi->get_notification_template_admin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **template_dto** | [**TemplateDto**](TemplateDto.md)|  | 

### Return type

[**TemplateResponseDto**](TemplateResponseDto.md)

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

# **send_test_email_admin**
> TestEmailResponseDto send_test_email_admin(admin_config_smtp_dto)

Send test email

Send a test email using the provided SMTP configuration.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.admin_config_smtp_dto import AdminConfigSmtpDto
from immich_sdk.models.test_email_response_dto import TestEmailResponseDto
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
    api_instance = immich_sdk.NotificationsAdminApi(api_client)
    admin_config_smtp_dto = immich_sdk.AdminConfigSmtpDto() # AdminConfigSmtpDto | 

    try:
        # Send test email
        api_response = api_instance.send_test_email_admin(admin_config_smtp_dto)
        print("The response of NotificationsAdminApi->send_test_email_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationsAdminApi->send_test_email_admin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **admin_config_smtp_dto** | [**AdminConfigSmtpDto**](AdminConfigSmtpDto.md)|  | 

### Return type

[**TestEmailResponseDto**](TestEmailResponseDto.md)

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


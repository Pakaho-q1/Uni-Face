# immich_sdk.AuthenticationApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**change_password**](AuthenticationApi.md#change_password) | **POST** /auth/change-password | Change password
[**change_pin_code**](AuthenticationApi.md#change_pin_code) | **PUT** /auth/pin-code | Change pin code
[**finish_o_auth**](AuthenticationApi.md#finish_o_auth) | **POST** /oauth/callback | Finish OAuth
[**get_auth_status**](AuthenticationApi.md#get_auth_status) | **GET** /auth/status | Retrieve auth status
[**link_o_auth_account**](AuthenticationApi.md#link_o_auth_account) | **POST** /oauth/link | Link OAuth account
[**lock_auth_session**](AuthenticationApi.md#lock_auth_session) | **POST** /auth/session/lock | Lock auth session
[**login**](AuthenticationApi.md#login) | **POST** /auth/login | Login
[**logout**](AuthenticationApi.md#logout) | **POST** /auth/logout | Logout
[**logout_o_auth**](AuthenticationApi.md#logout_o_auth) | **POST** /oauth/backchannel-logout | Backchannel OAuth logout
[**redirect_o_auth_to_mobile**](AuthenticationApi.md#redirect_o_auth_to_mobile) | **GET** /oauth/mobile-redirect | Redirect OAuth to mobile
[**reset_pin_code**](AuthenticationApi.md#reset_pin_code) | **DELETE** /auth/pin-code | Reset pin code
[**setup_pin_code**](AuthenticationApi.md#setup_pin_code) | **POST** /auth/pin-code | Setup pin code
[**sign_up_admin**](AuthenticationApi.md#sign_up_admin) | **POST** /auth/admin-sign-up | Register admin
[**start_o_auth**](AuthenticationApi.md#start_o_auth) | **POST** /oauth/authorize | Start OAuth
[**unlink_o_auth_account**](AuthenticationApi.md#unlink_o_auth_account) | **POST** /oauth/unlink | Unlink OAuth account
[**unlock_auth_session**](AuthenticationApi.md#unlock_auth_session) | **POST** /auth/session/unlock | Unlock auth session
[**validate_access_token**](AuthenticationApi.md#validate_access_token) | **POST** /auth/validateToken | Validate access token


# **change_password**
> UserAdminResponseDto change_password(change_password_dto)

Change password

Change the password of the current user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.change_password_dto import ChangePasswordDto
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    change_password_dto = immich_sdk.ChangePasswordDto() # ChangePasswordDto | 

    try:
        # Change password
        api_response = api_instance.change_password(change_password_dto)
        print("The response of AuthenticationApi->change_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->change_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **change_password_dto** | [**ChangePasswordDto**](ChangePasswordDto.md)|  | 

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

# **change_pin_code**
> change_pin_code(pin_code_change_dto)

Change pin code

Change the pin code for the current user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.pin_code_change_dto import PinCodeChangeDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    pin_code_change_dto = immich_sdk.PinCodeChangeDto() # PinCodeChangeDto | 

    try:
        # Change pin code
        api_instance.change_pin_code(pin_code_change_dto)
    except Exception as e:
        print("Exception when calling AuthenticationApi->change_pin_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pin_code_change_dto** | [**PinCodeChangeDto**](PinCodeChangeDto.md)|  | 

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

# **finish_o_auth**
> LoginResponseDto finish_o_auth(o_auth_callback_dto)

Finish OAuth

Complete the OAuth authorization process by exchanging the authorization code for a session token.

### Example


```python
import immich_sdk
from immich_sdk.models.login_response_dto import LoginResponseDto
from immich_sdk.models.o_auth_callback_dto import OAuthCallbackDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    o_auth_callback_dto = immich_sdk.OAuthCallbackDto() # OAuthCallbackDto | 

    try:
        # Finish OAuth
        api_response = api_instance.finish_o_auth(o_auth_callback_dto)
        print("The response of AuthenticationApi->finish_o_auth:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->finish_o_auth: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **o_auth_callback_dto** | [**OAuthCallbackDto**](OAuthCallbackDto.md)|  | 

### Return type

[**LoginResponseDto**](LoginResponseDto.md)

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

# **get_auth_status**
> AuthStatusResponseDto get_auth_status()

Retrieve auth status

Get information about the current session, including whether the user has a password, and if the session can access locked assets.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.auth_status_response_dto import AuthStatusResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)

    try:
        # Retrieve auth status
        api_response = api_instance.get_auth_status()
        print("The response of AuthenticationApi->get_auth_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->get_auth_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AuthStatusResponseDto**](AuthStatusResponseDto.md)

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

# **link_o_auth_account**
> UserAdminResponseDto link_o_auth_account(o_auth_callback_dto)

Link OAuth account

Link an OAuth account to the authenticated user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.o_auth_callback_dto import OAuthCallbackDto
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    o_auth_callback_dto = immich_sdk.OAuthCallbackDto() # OAuthCallbackDto | 

    try:
        # Link OAuth account
        api_response = api_instance.link_o_auth_account(o_auth_callback_dto)
        print("The response of AuthenticationApi->link_o_auth_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->link_o_auth_account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **o_auth_callback_dto** | [**OAuthCallbackDto**](OAuthCallbackDto.md)|  | 

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

# **lock_auth_session**
> lock_auth_session()

Lock auth session

Remove elevated access to locked assets from the current session.

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
    api_instance = immich_sdk.AuthenticationApi(api_client)

    try:
        # Lock auth session
        api_instance.lock_auth_session()
    except Exception as e:
        print("Exception when calling AuthenticationApi->lock_auth_session: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

# **login**
> LoginResponseDto login(login_credential_dto)

Login

Login with username and password and receive a session token.

### Example


```python
import immich_sdk
from immich_sdk.models.login_credential_dto import LoginCredentialDto
from immich_sdk.models.login_response_dto import LoginResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    login_credential_dto = immich_sdk.LoginCredentialDto() # LoginCredentialDto | 

    try:
        # Login
        api_response = api_instance.login(login_credential_dto)
        print("The response of AuthenticationApi->login:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->login: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login_credential_dto** | [**LoginCredentialDto**](LoginCredentialDto.md)|  | 

### Return type

[**LoginResponseDto**](LoginResponseDto.md)

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

# **logout**
> LogoutResponseDto logout()

Logout

Logout the current user and invalidate the session token.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.logout_response_dto import LogoutResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)

    try:
        # Logout
        api_response = api_instance.logout()
        print("The response of AuthenticationApi->logout:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->logout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**LogoutResponseDto**](LogoutResponseDto.md)

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

# **logout_o_auth**
> logout_o_auth(logout_token)

Backchannel OAuth logout

Logout the OAuth account and invalidate the session specified by the sid claim or all sessions if the sid claim is not present.

### Example


```python
import immich_sdk
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    logout_token = 'logout_token_example' # str | OAuth logout token

    try:
        # Backchannel OAuth logout
        api_instance.logout_o_auth(logout_token)
    except Exception as e:
        print("Exception when calling AuthenticationApi->logout_o_auth: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **logout_token** | **str**| OAuth logout token | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **redirect_o_auth_to_mobile**
> redirect_o_auth_to_mobile()

Redirect OAuth to mobile

Requests to this URL are automatically forwarded to the mobile app, and is used in some cases for OAuth redirecting.

### Example


```python
import immich_sdk
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
    api_instance = immich_sdk.AuthenticationApi(api_client)

    try:
        # Redirect OAuth to mobile
        api_instance.redirect_o_auth_to_mobile()
    except Exception as e:
        print("Exception when calling AuthenticationApi->redirect_o_auth_to_mobile: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_pin_code**
> reset_pin_code(pin_code_reset_dto)

Reset pin code

Reset the pin code for the current user by providing the account password

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.pin_code_reset_dto import PinCodeResetDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    pin_code_reset_dto = immich_sdk.PinCodeResetDto() # PinCodeResetDto | 

    try:
        # Reset pin code
        api_instance.reset_pin_code(pin_code_reset_dto)
    except Exception as e:
        print("Exception when calling AuthenticationApi->reset_pin_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pin_code_reset_dto** | [**PinCodeResetDto**](PinCodeResetDto.md)|  | 

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

# **setup_pin_code**
> setup_pin_code(pin_code_setup_dto)

Setup pin code

Setup a new pin code for the current user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.pin_code_setup_dto import PinCodeSetupDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    pin_code_setup_dto = immich_sdk.PinCodeSetupDto() # PinCodeSetupDto | 

    try:
        # Setup pin code
        api_instance.setup_pin_code(pin_code_setup_dto)
    except Exception as e:
        print("Exception when calling AuthenticationApi->setup_pin_code: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pin_code_setup_dto** | [**PinCodeSetupDto**](PinCodeSetupDto.md)|  | 

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

# **sign_up_admin**
> UserAdminResponseDto sign_up_admin(sign_up_dto)

Register admin

Create the first admin user in the system.

### Example


```python
import immich_sdk
from immich_sdk.models.sign_up_dto import SignUpDto
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    sign_up_dto = immich_sdk.SignUpDto() # SignUpDto | 

    try:
        # Register admin
        api_response = api_instance.sign_up_admin(sign_up_dto)
        print("The response of AuthenticationApi->sign_up_admin:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->sign_up_admin: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sign_up_dto** | [**SignUpDto**](SignUpDto.md)|  | 

### Return type

[**UserAdminResponseDto**](UserAdminResponseDto.md)

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

# **start_o_auth**
> OAuthAuthorizeResponseDto start_o_auth(o_auth_config_dto)

Start OAuth

Initiate the OAuth authorization process.

### Example


```python
import immich_sdk
from immich_sdk.models.o_auth_authorize_response_dto import OAuthAuthorizeResponseDto
from immich_sdk.models.o_auth_config_dto import OAuthConfigDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    o_auth_config_dto = immich_sdk.OAuthConfigDto() # OAuthConfigDto | 

    try:
        # Start OAuth
        api_response = api_instance.start_o_auth(o_auth_config_dto)
        print("The response of AuthenticationApi->start_o_auth:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->start_o_auth: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **o_auth_config_dto** | [**OAuthConfigDto**](OAuthConfigDto.md)|  | 

### Return type

[**OAuthAuthorizeResponseDto**](OAuthAuthorizeResponseDto.md)

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

# **unlink_o_auth_account**
> UserAdminResponseDto unlink_o_auth_account()

Unlink OAuth account

Unlink the OAuth account from the authenticated user.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.user_admin_response_dto import UserAdminResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)

    try:
        # Unlink OAuth account
        api_response = api_instance.unlink_o_auth_account()
        print("The response of AuthenticationApi->unlink_o_auth_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->unlink_o_auth_account: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserAdminResponseDto**](UserAdminResponseDto.md)

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

# **unlock_auth_session**
> unlock_auth_session(session_unlock_dto)

Unlock auth session

Temporarily grant the session elevated access to locked assets by providing the correct PIN code.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.session_unlock_dto import SessionUnlockDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)
    session_unlock_dto = immich_sdk.SessionUnlockDto() # SessionUnlockDto | 

    try:
        # Unlock auth session
        api_instance.unlock_auth_session(session_unlock_dto)
    except Exception as e:
        print("Exception when calling AuthenticationApi->unlock_auth_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_unlock_dto** | [**SessionUnlockDto**](SessionUnlockDto.md)|  | 

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

# **validate_access_token**
> ValidateAccessTokenResponseDto validate_access_token()

Validate access token

Validate the current authorization method is still valid.

### Example

* Api Key Authentication (cookie):
* Api Key Authentication (api_key):
* Bearer (JWT) Authentication (bearer):

```python
import immich_sdk
from immich_sdk.models.validate_access_token_response_dto import ValidateAccessTokenResponseDto
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
    api_instance = immich_sdk.AuthenticationApi(api_client)

    try:
        # Validate access token
        api_response = api_instance.validate_access_token()
        print("The response of AuthenticationApi->validate_access_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AuthenticationApi->validate_access_token: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ValidateAccessTokenResponseDto**](ValidateAccessTokenResponseDto.md)

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


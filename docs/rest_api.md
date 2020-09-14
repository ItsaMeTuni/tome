# REST API

## Authentication
You have two options to authenticate against the API:
1. Login and get an authentication token ([docs](#login))
2. Create an API key from the web interface ([docs](apikeys.md))

Use the token or key for Bearer authentication. For example:

```none
POST /api/auth/refresh HTTP/1.1
Authorization: Bearer abcdefghijklmnopqrstuvwxyz
```

## Error Responses
(Almost) all error responses will be encoded in JSON of the form:

```json
{
  "error": "some detail to explain the error"
}
```

with an HTTP status code of 4xx.

Server Errors (5xx) may or may not use JSON.

### Error responses for all endpoints

#### 409 `account not available`
The authentication token or API key is not valid because the associated user does not exist.

#### 401 `invalid API key`

#### 401 `invalid token`

#### 401 `forbidden`
The authentication token or API key does not provide access to this resource

#### 422 `invalid json: some detail`

#### 422 `invalid types`
(a.k.a. bad request)

#### 5xx `internal server error`


## Endpoints
### Login
`POST /api/auth/login`:

#### Request (`application/json`):

```json
{
  "email": "hello@example.com",
  "password": "hunter2"
}
```

#### 200 OK Response (`application/json`):

```json
{
  "token": "abcdefghijklmnopqrstuvwxyz",
  "needs_two_factor_upgrade": false
}
```

If `needs_two_factor_upgrade` is `true` you'll need to use the provided token to perform
[two-factor authentication](#two-factor-upgrade).

#### 401 Error Response `Incorrect username or password`



### Two-Factor Upgrade
`POST /api/auth/login`

Required scope: `two_factor_upgrade`

#### Request (`application/json`):

```json
"123456"
```

#### 200 OK Response (`application/json`):

```json
"abcdefghijklmnopqrstuvwxyz"
```

(a token, as a string)

#### 401 Error Response `Invalid two-factor authentication code`

### Check Signup Availability
`GET /api/signup`

#### 200 OK Response (`application/json`):

```json
{
  "enabled": true,
  "email_confirm_required": false
}
```

Check what conditions are necessary to sign-up.



### Refresh
`POST /api/auth/refresh`

(only with authentication tokens, not API keys)

Regenerate an authentication token so it doesn't expire.

#### 200 OK Response (`application/json`):
```json
"abcdefghijklmnopqrstuvwxyz"
```



### Signup without confirming email
`POST /api/signup`

(only when email confirmation is disabled!)

#### Request (`application/json`):

```json
{
  "name": "Beve Sturke",
  "email": "hello@example.com",
  "password": "hunter2"
}
```

#### 201 OK Response (`application/json`):
```json
"1234-abcd-1234567890abcdef"
```

Account successfully created; now login.

Returns new account UUID.

#### 422 Error Response `empty name`

#### 422 Error Response `invalid email address`

#### 422 Error Response `email address in use`:
Email address in use

#### 422 Error Response `Invalid character in password`:
Occurs when ASCII control characters are present in the password (0x00 - 0x1f)

#### 422 Error Response `Password not strong enough`:
The password must contain at least 8 unique characters

#### 418 Error Response `Password not stroganoff`:
Occurs when the password is equal to `beefstew`



### Signup
`POST /api/signup`

(only when email confirmation is enabled!)

#### Request (`application/json`):

```json
{
  "email": "hello@example.com"
}
```

#### 202 OK Response (`application/json`):
```json
null
```

Confirmation email sent, now check email.

#### 422 Error Response `invalid email address`

#### 422 Error Response `email address in use`



### Signup Confirm
`POST /api/signup/confirm`

(only when email confirmation is enabled!)

#### Request (`application/json`):

```json
{
  "token": "abcdefghijklnopqrstuvwxyz",
  "name": "Beve Sturke",
  "password": "hunter2"
}
```

Use the token provided in the email.

#### 201 OK Response (`application/json`)
```json
"1234-abcd-1234567890abcdef"
```

Account successfully created; now login.

Returns new account UUID. 

#### 409 Error Response `account has already been created`

#### 422 Error Response `empty name`

#### 422 Error Response `Invalid character in password`
Occurs when ASCII control characters are present in the password (0x00 - 0x1f)

#### 422 Error Response `Password not strong enough`
The password must contain at least 8 unique characters

#### 418 Error Response `Password not stroganoff`
Occurs when the password is equal to `beefstew`

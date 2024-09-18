# 0x01. Basic authentication
`Back-end` `Authentication`

In this project, you will learn what the authentication process means and implement **Basic Authentication ** on a simple API

## Resources
** Read or watch:**
* [REST API Authentication Mechanisms](REST API Authentication Mechanisms)
* [Base64 in Python](https://docs.python.org/3.7/library/base64.html)
* [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
* [Flask](https://palletsprojects.com/projects/flask/)
* [Base64 - concept](https://en.wikipedia.org/wiki/Base64)

## Tasks
### 0.Simple-basic-API

## Setup and start server
```
bob@dylan:~$ pip3 install -r requirements.txt
...
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Serving Flask app "app" (lazy loading)
...
bob@dylan:~$
```
##Use the API(in another tab or in your browser)
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/status HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 16
< Access-Control-Allow-Origin: *
< Server: Werkzeug/1.0.1 Python/3.7.5
< Date: Mon, 18 May 2020 20:29:21 GMT
< 
{"status":"OK"}
* Closing connection 0
bob@dylan:~$
```

### 1. Error handler: Unauthorized
What the HTTP status code for a request unauthorized? `401` of course!
Edit `api/v1/app.py`
* Add a new error handler for this status code, the response must be:
	* a JSON: {"error": "Unauthorized"}
	* status code `401`
	* you must use `jsonify` from Flask
For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:
* Route: `Get /api/v1/unauthorized`
* This endpoint must raise a 401 error by using `abort` - [Custom Error Pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)

By calling `abort(401)`, the error handler for 401 will be executed.

In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/unauthorized HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:50:40 GMT
< 
{
  "error": "Unauthorized"
}
* Closing connection 0
bob@dylan:~$
```

### 2. Error handler: Forbidden
What the HTTP status code for a request where the user is authenticate but not allowed to access to a resource? `403` of course
Edit `api/v1/app.py`:
* Add a new error handler for this code, the response must be:
	* a JSON: `{"error": "Forbidden"}`
	* status code 403
	* you must use `jsonify` from Flask
For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:
* Route: `GET /api/v1/forbidden`
* This endpoint must raise a 403 error by using `abort` - [Custom Error Pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)
t
By calling `abort(403)`, the error handler for 403 will be executed.

In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden"
{
  "error": "Forbidden"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/forbidden HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 403 FORBIDDEN
< Content-Type: application/json
< Content-Length: 27
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:54:22 GMT
< 
{
  "error": "Forbidden"
}
* Closing connection 0
bob@dylan:~$
```
### 3. Auth class
Now you will create a class to manage the API authentication.
* Create a folder `api/v1/auth`
* Create an empty file `api/v1/auth/__init__.py
* Create the class `Auth`:
        * in the file `api/v1/auth`auth.py`
        * import `request` from `flask`
        * class name `Auth`
        * public method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` that returns `False` - `path` and `excluded_paths` will be used later,now,you don't need to take care of them
	* public method `def authorization_header(self, request=None) -> str:` that returns `None` - `request` will be the Flask request object
	* public method `def current_user(self, request=None) -> TypeVar('User'):` that returns `None` - `request` will be the Flask request object
This class is the template for all authentication system you will implement.
```
bob@dylan:~$ cat main_0.py
#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())

bob@dylan:~$ 
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_0.py
False
None
None
bob@dylan:~$
```

### 4. Define which routes don't need authentication
Update the method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool: ` in `Auth` that returns `True` if the `path` is not in the list of strings `excluded_paths`:
* Returns `True` if `path` is `None`
* Returns `True` if `excluded_paths`
* Return `False` if `path` is in `exclude_paths`
* You can assume `excluded_paths` contains string path always ending by a `/`
* This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/`must be returned `False` if `excluded_path` contains `/api/v1/status/` must be returned `False` if `excluded_paths` contains `/api/v1/status/`
```
bob@dylan:~$ cat main_1.py
#!/usr/bin/env python3
""" Main 1
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth(None, None))
print(a.require_auth(None, []))
print(a.require_auth("/api/v1/status/", []))
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))

bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_1.py
True
True
True
False
False
True
True
bob@dylan:~$
```
### 5. Request validation!
Now you will validate all requests to secure the API:
Update the method `def authorization_header(self, request=None) -> str:`in `api/v1/auth/auth.py`:
* If `request` is `None`, returns `None`
* If `request` doesn't contain the header key `Authorization`, returns `None`
* Otherwise, return the value of the header request `Authorization`
Update the file `api/v1/app.py`:
* Create a variable `auth` initialized to `None` after the `CORS` definitions
* Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to auth
	* if `auth`
		* import `Auth` from `api.v1.auth.auth`
		* create an instance of `Auth` and assign it to the variable `auth`
Now the biggest piece is the filtering of each request. For that you will use the Flask method [before_request](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint.before_request)
* Add a method in `api/v1/app.py` to handler `before_request`
	* if `auth` is `None`, do nothing
	* if `request.path` is not part of this list `['/api/v1/status/', '/api/v1/unauthorized', '/api/v1/forbidden/']`, do nothing - you must use the method `require_auth` from the `auth` instance
	* if `auth.authorization_header(request)` returns `None`, raise the error `401` - you must use `abort`
In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```
### 6. Basic auth
Create a class `BasicAuth` that inherits from `Auth`. For the moment this class will be empty.
Update `api/v1/app.py for using `BasicAuth` class instead of `Auth` depending of the value of the environment variable `AUTH_TYPE`, If `AUTH_TYPE` is equal to `basic_auth`:
* import `BasicAuth` from `api.v1.auth.basic_auth
* create an instance of `BasicAuth` and assign it to the variable `auth`
Otherwise, keep the previous mechanism with `auth` an instance of `Auth`.
In the first terminal:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```
### 7. Basic - Base64 part
Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class `BasicAuth` that returns the Base64 part of the `Authorization` header for a Basic Authentication:
* Return `None` if `authorization_header` is `None`
* Return `None` if `authorization_header` is not a string
* Return `None` if `authorization_header` doesn't start by `Basic` (with a space at the end)
* Otherwise, return the value after `Basic`(after the space)
* You can assume `authorization_header` contains only one `Basic`
```
### 8. Basic - Base64 decode
Add the method `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:` in the class `BasicAuth` that returns the decoded value of a Base64 string `base64_authorization_header`:
* Return `None` if `authorization_header` is `None`
* Return `None` if `authorization_header` is not a string
* Return `None` if `authorization_header` is not a valid Base64 - you can use `try/except`
* Othewise, return the decoded value as UTF8 string - you can user `decode('utf-8')`
```
bob@dylan:~$ cat main_3.py
#!/usr/bin/env python3
""" Main 3
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.decode_base64_authorization_header(None))
print(a.decode_base64_authorization_header(89))
print(a.decode_base64_authorization_header("Holberton School"))
print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))

bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_3.py
None
None
None
Holberton
Holberton School
Holberton School
bob@dylan:~$
bob@dylan:~$ cat main_3.py
#!/usr/bin/env python3
""" Main 3
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.decode_base64_authorization_header(None))
print(a.decode_base64_authorization_header(89))
print(a.decode_base64_authorization_header("Holberton School"))
print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
print(a.decode_base64_aution_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))

bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_3.py
None
None
None
Holberton
Holberton School
Holberton School
bob@dylan:~$

Return None if base64_authorization_header is None
Return None if base64_authorization_header is not a string
Return None if base64_authorization_header is not a valid Base64 - you can use try/except
Otherwise, return the decoded value as UTF8 string - you can use decode('utf-8')
bob@dylan:~$ cat main_2.py
#!/usr/bin/env python3
""" Main 2
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authoriza

## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)




<p align="center"><img src="./assets/TP-RequestFlows.png" height=200></p>

# TP-RequestFlows - PyPI
_A Python library for sending raw HTTP requests in a predefined sequence configured via a rules.json file. Supports automatic re-login when the session token expires_

<p align="center">
	<a href="https://github.com/tpcybersec/TP-RequestFlows/releases/"><img src="https://img.shields.io/github/release/tpcybersec/TP-RequestFlows" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/downloads/tpcybersec/TP-RequestFlows/total" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/stars/tpcybersec/TP-RequestFlows" height=30></a>
	<a href="#"><img src="https://img.shields.io/github/forks/tpcybersec/TP-RequestFlows" height=30></a>
	<a href="https://github.com/tpcybersec/TP-RequestFlows/issues?q=is%3Aopen+is%3Aissue"><img src="https://img.shields.io/github/issues/tpcybersec/TP-RequestFlows" height=30></a>
	<a href="https://github.com/tpcybersec/TP-RequestFlows/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/tpcybersec/TP-RequestFlows" height=30></a>
	<br>
	<a href="#"><img src="https://img.shields.io/pypi/v/TP-RequestFlows" height=30></a>
	<a href="#"><img src="https://img.shields.io/pypi/dm/TP-RequestFlows" height=30></a>
</p>

---
## Installation
#### From PyPI:
```console
pip install TP-RequestFlows
```
#### From Source:
```console
git clone https://github.com/tpcybersec/TP-RequestFlows.git --branch <Branch/Tag>
cd TP-RequestFlows
python setup.py build
python setup.py install
```

---
## Basic Usage
### run_flows(
  ```python
  FlowFolder,
  add_object = dict(),
  update_object = dict(),
  delete_object = dict(),
  ReqTimeout = 60,
  ReqDelaytime = 0,
  sleeptime = 20,
  separator = "||",
  parse_index = "$",
  dupSign_start = "{{{",
  dupSign_end = "}}}",
  ordered_dict = False,
  update_content_length = True,
  proxy_server = None,
  verbose = True
  ```
)
- `FlowFolder`: Path to the folder containing raw HTTP request files (`raw-[reqNum].req`) and the `rules.json` file.

  Example folder structure:
  ```
  FlowName/
  ├── raw-1.req
  ├── raw-2.req
  ├── raw-[reqNum].req
  └── rules.json
  ```
- `add_object`: Add parameters to `QueryParams`, `HTTPHeaders`, `HTTPCookies`, `RequestBody` of requests at runtime.
- `update_object`: Update parameter values for `RequestMethod`, `RequestPath`, `PathParams`, `QueryParams`, `RequestFragment`, `HTTPVersion`, `HTTPHeaders`, `HTTPCookies`, `RequestBody` of requests at runtime.
- `delete_object`: Remove parameters from `QueryParams`, `HTTPHeaders`, `HTTPCookies`, `RequestBody` of requests at runtime.
- `ReqTimeout`: Timeout in seconds for each HTTP request.
- `ReqDelaytime`: Delay (in seconds) between consecutive requests.
- `sleeptime`: If response time exceeds or equals this value, the RT will be highlighted in red.
- `separator`, `parse_index`, `dupSign_start`, `dupSign_end`, `ordered_dict`: Refer to the [json-duplicate-keys](https://github.com/truocphan/json-duplicate-keys) project for handling complex JSON with duplicate keys.
- `update_content_length`: Automatically updates the `Content-Length` header when modified.
- `proxy_server`: Proxy configuration for sending requests. Format: `{ "host": "PROXY-HOST", "port": PROXY-PORT }`.
- `verbose`: Show debug information and request status during execution.

### Detailed configuration of `rules.json`
The `rules.json` file defines the flow logic and dynamic behavior for the sequence of raw HTTP requests. It consists of three primary sections:
- `environments`: Configure reusable variables and import Python modules.
- `flows`: Define each HTTP request and how parameters are dynamically populated.
- `PATTERN_SuccessFlows` (optional): Regex used to verify a successful response.
##### Structure overview:
```
{
  "environments": {
    "libs": [ ... ],
    "vars": { ... }
  },
  "flows": {
    "[reqNum]": {
      "Host": "...",
      "Port": ...,
      "Scheme": "...",
      "PathParams": { ... },
      "QueryParams": { ... },
      "HTTPHeaders": { ... },
      "HTTPCookies": { ... },
      "RequestBody": { ... }
    },
    ...
  },
  "PATTERN_SuccessFlows": "..."
}
```
##### Section details:
- `environments`
  - `libs` (optional): A list of Python modules to dynamically import. Useful for using built-in functions or custom logic in variable definitions.
    ```
    "libs": [
      "import re",
      "from urllib.parse import quote"
    ]
    ```
  - `vars`: Define reusable variables, either static or dynamically extracted from previous responses. Each variable consists of:
    - `value`: A static string or Python expression.
    - `runCode`: Set to true if value is a Python expression that should be evaluated at runtime. **Note**: When `runCode: true`, the expression has access to: _`Flows`: A dictionary containing all previous request/response data_ and _Python libraries listed in libs._
    ```
    "vars": {
      "csrf_token": {
        "value": "re.search('name=\"csrf\" value=\"(.*?)\"', Flows['1']['rawResponse']).group(1)",
        "runCode": true
      },
      "static_user": {
        "value": "admin",
        "runCode": false
      }
    }
    ```
- `flows`: The `flows` section defines the actual HTTP request sequence. Each key ("1", "2", ...) represents a request step and contains request components such as host, port, headers, body, and more.
  ```
  "1": {
    "Host": "example.com",
    "Port": 443,
    "Scheme": "https",
    "PathParams": {
      "userId": "{user_id}"
    },
    "QueryParams": {
      "page": "1"
    },
    "HTTPHeaders": {
      "Authorization": "Bearer {access_token}"
    },
    "HTTPCookies": {
      "session": "abc123"
    },
    "RequestBody": {
      "name": "John Doe",
      "email": "{user_email}"
    }
  }
  ```
  **Common fields**:
  | Field         | Description                                              |
  | ------------- | -------------------------------------------------------- |
  | `Host`        | Target host name (e.g. `"example.com"`)                  |
  | `Port`        | Target port (e.g. `443` for HTTPS)                       |
  | `Scheme`      | Either `"http"` or `"https"`                             |
  | `PathParams`  | Values to replace path variables (e.g. `/user/<userId>`) |
  | `QueryParams` | URL query parameters (e.g. `?page=2`)                    |
  | `HTTPHeaders` | HTTP headers to include                                  |
  | `HTTPCookies` | Cookies to include in the request                        |
  | `RequestBody` | Request payload for POST/PUT requests                    |

  Placeholders in the form `{varName}` are automatically replaced with variables from `environments.vars`.
- `PATTERN_SuccessFlows` (optional): Defines a regular expression used to check whether the flow executed successfully. This regex is applied to the raw response body of the last flow.
  ```
  "PATTERN_SuccessFlows": "Welcome, admin"
  ```
  If the pattern matches, the response is considered successful. Useful in automation and scripting scenarios.

---
## Advanced Usage
### AutoLogin - Automatic Re-login on Session Expiry
The `AutoLogin` feature in **TP-RequestFlows** allows the tool to automatically detect session expiration and re-authenticate by executing a predefined login flow. It extracts new session-related values (such as cookies or tokens) and retries the failed request using updated credentials — without any manual intervention
##### How AutoLogin Works
The AutoLogin process consists of three core components:
- `ObtainSessionTokenFlow`: Path to a folder that contains the login flow used to re-authenticate. This folder must include a `rules.json` file and one or more `raw-*.req` files representing the login requests.
- `Matcher`: Determines whether the session is considered expired based on the response content of any flow step
  - `PATTERN`: A list of regular expressions applied to the response (including headers and body).
  - `CONDITION`: Either `"AND"` or `"OR"`
    - `"AND"`: All patterns must match.
    - `"OR"`: At least one pattern must match.
- `Extractors`: Python expressions that extract tokens or session cookies from the login flow response. These expressions are evaluated at runtime and use the special variable `Flows_AutoLogin`, which stores the raw request/response data of the login flow.
  - Example:
    ```
    TP_HTTP_RESPONSE_PARSER(Flows_AutoLogin['2']['rawResponse']).response_cookies.get('session')['value']
    ```
##### Example Configuration
  ```
  "AutoLogin": {
    "ObtainSessionTokenFlow": ".\\TestData\\Flows\\Gin_Juice_Shop\\Login",
    "Matcher": {
      "CONDITION": "AND",
      "PATTERN": [
        "HTTP/(1\\.1|2) 302 Found",
        "Location: /login"
      ]
    },
    "Extractors": {
      "AWSALB": "TP_HTTP_RESPONSE_PARSER(Flows_AutoLogin['2']['rawResponse']).response_cookies.get('AWSALB')['value']",
      "AWSALBCORS": "TP_HTTP_RESPONSE_PARSER(Flows_AutoLogin['2']['rawResponse']).response_cookies.get('AWSALBCORS')['value']",
      "session": "TP_HTTP_RESPONSE_PARSER(Flows_AutoLogin['2']['rawResponse']).response_cookies.get('session')['value']"
    }
  }
  ```
##### Variable Scope and Usage
- All values extracted by the `Extractors` section are injected into the global variable scope under the special namespace `AUTO_LOGIN`.
- To use them in your main flow, reference them using the syntax: `AUTO_LOGIN||<varName>`
- Example:
  ```
  "HTTPCookies": {
    "session": "AUTO_LOGIN||session"
  }
  ```
  This tells the engine to use the session cookie obtained during AutoLogin instead of a static value

### add_object - Add new parameters dynamically at runtime
The `add_object` parameter allows you to dynamically add new key-value pairs into specific components of any request in the flow, without modifying the original raw file or `rules.json`
##### Structure:
  ```
  add_object = {
    "1": {
      "QueryParams": {
        "newQueryParam-Name1": value1,
        "newQueryParam-Name2": value2,
        ...
      },
      "HTTPHeaders": {
        "newHTTPHeader-Name1": value1,
        "newHTTPHeader-Name2": value2,
        ...
      },
      "HTTPCookies": {
        "newHTTPCookie-Name1": value1,
        "newHTTPCookie-Name2": value2,
        ...
      },
      "RequestBody": {
        "newBodyParam-Name1": value1,
        "newBodyParam-Name2": value2,
        ...
      }
    },
    "[reqNum]": {
      "QueryParams": { ... },
      "HTTPHeaders": { ... },
      "HTTPCookies": { ... },
      "RequestBody": { ... }
    },
    ...
  }
  ```
  - The top-level keys (`"1"`, `"2"`, ...) correspond to the flow step (i.e., request number).
  - Each inner object can contain one or more of:
    - `QueryParams`
    - `HTTPHeaders`
    - `HTTPCookies`
    - `RequestBody`
  - Values can be:
    - Static strings (e.g., `"test123"`).
    - Variable name (e.g., `csrf_token`).
##### Example:
  ```
  add_object = {
    "1": {
      "QueryParams": {
        "debug": "true"
      },
      "HTTPHeaders": {
        "X-Custom-Header": "InjectedValue"
      }
    },
    "3": {
      "RequestBody": {
        "extraField": csrf_token
      }
    }
  }
  ```
  This will:
    - Add `debug=true` to the query string of request `1`.
    - Inject `X-Custom-Header: InjectedValue` into headers of request `1`.
    - Add an `extraField` to the request body of request `3` using a variable name `csrf_token`.

### `update_object` – Modify existing parameters in real-time
The `update_object` parameter allows you to dynamically change existing values of various components in a request, overriding what's defined in the raw files or `rules.json`
##### Structure:
  ```
  update_object = {
    "1": {
      "RequestMethod": "request method",
      "RequestPath": "request path",
      "PathParams": {
        "PathParam-Name1": value1,
        "PathParam-Name2": value2,
        ...
      },
      "QueryParams": {
        "QueryParam-Name1": value1,
        "QueryParam-Name2": value2,
        ...
      },
      "RequestFragment": "request fragment",
      "HTTPVersion": " http version",
      "HTTPHeaders": {
        "HTTPHeader-Name1": value1,
        "HTTPHeader-Name2": value2,
        ...
      },
      "HTTPCookies": {
        "HTTPCookie-Name1": value1,
        "HTTPCookie-Name2": value2,
        ...
      },
      "RequestBody": {
        "BodyParam-Name1": value1,
        "BodyParam-Name2": value2,
        ...
      }
    },
    "[reqNum]": {
      "RequestMethod": "...",
      "RequestPath": "...",
      "PathParams": { ... },
      "QueryParams": { ... },
      "RequestFragment": "...",
      "HTTPVersion": "...",
      "HTTPHeaders": { ... },
      "HTTPCookies": { ... },
      "RequestBody": { ... }
    },
    ...
  }
  ```
  - The top-level keys (`"1"`, `"2"`, ...) refer to request numbers.
  - Fields listed will replace existing values with the new ones provided.
##### Example:
  ```
  update_object = {
    "2": {
      "RequestMethod": "PUT",
      "QueryParams": {
        "sort": "desc"
      },
      "HTTPHeaders": {
        "User-Agent": "MyCustomAgent/1.0"
      }
    }
  }
  ```
  This will:
  - Change the HTTP method of request `2` to `PUT`.
  - Override `sort` query param with `"desc"`.
  - Replace the `User-Agent` header value with `"MyCustomAgent/1.0"`.

### `delete_object` – Remove specific parameters from requests
The `delete_object` parameter lets you delete specific keys from request components (Query, Header, Cookie, Body), which is useful for stripping out unnecessary or sensitive data
##### Structure:
  ```
  delete_object = {
    "1": {
      "QueryParams": [
        "QueryParam-Name1",
        "QueryParam-Name2",
        ...
      ],
      "HTTPHeaders": [
        "HTTPHeader-Name1",
        "HTTPHeader-Name2",
        ...
      ],
      "HTTPCookies": [
        "HTTPCookie-Name1",
        "HTTPCookie-Name2",
        ...
      ],
      "RequestBody": [
        "BodyParam-Name1",
        "BodyParam-Name2",
        ...
      ]
    },
    "[reqNum]": {
      "QueryParams": [ ... ],
      "HTTPHeaders": [ ... ],
      "HTTPCookies": [ ... ],
      "RequestBody": [ ... ]
    },
    ...
  }
  ```
  - For each field, provide a list of keys to remove.
  - Only applicable to:
    - `QueryParams`
    - `HTTPHeaders`
    - `HTTPCookies`
    - `RequestBody`
##### Example:
  ```
  delete_object = {
    "1": {
      "QueryParams": ["debug"],
      "HTTPCookies": ["tracking_id"]
    }
  }
  ```
  This will:
  - Remove the `debug` query parameter from request `1`.
  - Remove the `tracking_id` cookie from request `1`.

---
## Contributors
<p align="left">
	<a href="https://github.com/h4x0rl33tx"><img src="https://avatars.githubusercontent.com/u/138019816" width="50" height="50" alt="h4x0rl33tx" style="max-width: 100%"></a>
</p>

---
## CHANGELOG
#### [TP-RequestFlows v2025.4.30](https://github.com/tpcybersec/TP-RequestFlows/tree/2025.4.30)
- **Raw Request Flow Execution** via `rules.json` and `raw-*.req` files.
- **Dynamic Variable Injection** using `{varName}` syntax in requests.
- **Python Expression Support** in variable definitions (`runCode: true`) with access to previous flows (`Flows`) and imported libs.
- **AutoLogin Mechanism**:
  - Detects session expiration using regex matchers.
  - Re-authenticates via a predefined login flow.
  - Injects new session values using `AUTO_LOGIN||<varName>` syntax.
- **Regex-Based Success Detection** using `PATTERN_SuccessFlows`.
- **Request Modification at Runtime**:
  - `add_object`: Inject new headers, params, cookies, or body fields.
  - `update_object`: Modify existing request components (method, headers, etc.).
  - `delete_object`: Strip specific fields from requests.
- **Proxy Support**: Optional proxy routing per request.
- **Automatic Content-Length Update** when body is modified.
- **Verbose Mode** for detailed runtime logging and debugging.
- **Custom Request Timing**:
  - `ReqTimeout`: Set request timeout.
  - `ReqDelaytime`: Delay between requests.
  - `sleeptime`: Highlight slow responses.
- **Duplicate JSON Keys** parsing via `json-duplicate-keys` module.
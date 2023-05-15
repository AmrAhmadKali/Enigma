## Sources

[IGNCore](https://gitlab.com/CynderGames/igncore), an own, heavily optimized hard-fork (Jan ~2021)
of [Tyrbot](https://github.com/Budabot/Tyrbot)
has been supplying Templates for various parts of the code. Mainly:

- Registry
- CommandParams
- DictObject
- CommandService

## Backend Usage

REQUESTS are to be sent using the following pattern:

## Requests

> `{"cmd": "set", "sub_cmd": "rotor", "params": [5, 10]}`

Where:

- `cmd` is the main command
- `sub_cmd` is the sub command, related to the main command. Optional
- `params` will contain all parameters required by the command, in order. Optional.

## Responses

> `{"status": "200", "response": ['Z']}`
> `{"status": 200, "response": [{"cmd": "help", "params": "", "desc": "This command will return an index of all available commands."}]}`

Where:

- `status` being any HTTP status code. For convenience, provided shortly.
- `response` will contain the response of the command. Optional.

### `status` might contain any of the following codes, with the listed meaning:

- 200 OK; The Request has been processed, no response.
- 300 Multiple Choices; The provided command had multiple matches, and could not be processed.
- 400 Bad Request; The Request was malformed, for example only 2 parameters for a command which requires 3
- 404 Not Found; the requested command is not registered on the backend
- 500 Internal Server Error; An unrecoverable error occurred on the backend, and the connection will be terminated by
  the server immediately.
- 501 Not Implemented; The requested command is registered on the backend, but its
-

### `response` might contain any of the following values:

- a list of dictionaries,
  like `[{"cmd": "help", "params": "", "desc": "This command will return an index of all available commands."}]`
- a list containing a single element, like `["A"]`


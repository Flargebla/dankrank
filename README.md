# DankRank

## Configuration

DankRank requires a new directory `danks` to be added to the root directory of the project. This is where all the images will be stored.

DankRank requires a file named `creds.json` to specify various connection credentials. The available keys and their required attributes are listed below:

### `reddit`
| Key | Description |
|---|---|
| `client_id` | The unique OAuth client identifier |
| `client_secret` | The OAuth client secret for the specific Reddit application |
| `username` | The username of the Reddit account |
| `user_agent` | The unique description of the application |
| `password` | The password of the Reddit account |

### Example
```
{
    "reddit":{
        "client_id"     :   "abcdefg",
        "client_secret" :   "thisisasecret",
        "user_agent"    :   "MyApp",
        "username"      :   "reddituser123",
        "password"      :   "password123"
    }
}
```

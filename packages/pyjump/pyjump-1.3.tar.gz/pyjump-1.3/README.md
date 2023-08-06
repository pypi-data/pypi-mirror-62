## Jump

### Intro 

Utility that builds a 2-level menu based on applications and their available environments. The setup that we have is that
this utility resides on a 'jump' server and every time a user connects to that server (via SSH), the menu script is 
executed. 

In our current setup, there is 2 kinds of servers: one type which has serverpilot installed and another one which is 
a vanilla ubuntu installation (both explained below)

This script also handles some applications/servers not being in the jumpgate.

The menu is built based on a JSON response from a server. The response looks like this:

```json
[
    {
        "id": "b84b07c8-738e-4088-969f-0ee4c822fd3a",
        "in_jumpgate": false,
        "name": "test-app",
        "servers": [
            {
                "display_name": "Staging",
                "id": "939bf2ce-d0e0-42b8-8600-f7f7ef5db72b",
                "ip": "1.2.3.4",
                "is_serverpilot": true,
                "name": "staging",
                "port": 222,
                "user": "serverpilot"
            },
            {
                "display_name": "Production",
                "id": "6a7f9169-5fe3-49d2-8eea-bfafcc53f4de",
                "ip": "1.2.3.4",
                "is_serverpilot": false,
                "name": "prod",
                "port": 222,
                "user": "root"
            }
        ]
    }, {
        "id": "81a1afa3-f610-4b64-935f-7e93c025209b",
        "in_jumpgate": true,
        "last_backup": 1538352010,
        "name": "another-test-app",
        "servers": [
            {
                "created_at": 1533644177,
                "display_name": "Staging",
                "id": "939bf2ce-d0e0-42b8-8600-f7f7ef5db72b",
                "ip": "1.2.3.4",
                "is_serverpilot": true,
                "name": "staging",
                "port": 222,
                "updated_at": 1533808205,
                "user": "serverpilot"
            }, {
                 "created_at": 1533644177,
                 "display_name": "Acceptance",
                 "id": "939bf2ce-d0e0-42b8-8600-f7f7ef5db72b",
                 "ip": "1.2.3.4",
                 "is_serverpilot": true,
                 "name": "acceptance",
                 "port": 222,
                 "updated_at": 1533808205,
                 "user": "serverpilot"
             }
        ]
    }
]
```

This creates a menu like so:

![](docs/img/app-menu.png)

Note that only the 2nd item is shown because the first one has the property `in_jumpgate` set to False. When you select
an app, you get a list of its available servers (environments):

![](docs/img/env-menu.png)

After selecting an item the SSH connection will be forwarded to that server.


### Installation

Before you install the jumpgate, you need to have the dialog package installed. You can install it either via brew if 
you're on MacOS or apt or yum or whatever.

You can install the jumpgate via pip:

`pip install pyjump`

By default, the jumpgate will look for a file called `.jump.env` in your home directory containing the following values:

- AUTH_KEY: If you use any kind of authentication when retrieving the items. If not, leave it empty.
- AUTH_HEADER: If you use authentication (via a header) set this to the value of your header.
- ENDPOINT: API endpoint from where to fetch the list of applications.

If you want to specify a different location for that file you can using the `--env-file` flag. Like so:

`jump --env-file=/other/location/.env`

### Usage

As mentioned above, there's 2 ways to use this. One is locally on your machine and another one is in one central server.
The latter is perfect for a team since every user just needs to ssh to the central server and everyone will see the same
applications and servers (for now it does not have permission-checking built in). 

#### Locally

If you'd like to run the script locally (assuming you've run the install script above), you just need to use `jump`.

#### On a central server

After installing the script, there's a couple things that you'd need to do.

- In `/etc/skel` create an .ssh folder and generate a privatey (and public) key with `ssh-keygen -t rsa`. What this will
do is have each created user have the same key when connecting to a remote server.
- Copy the generated key to any `authorized_keys` file on any server(s) you want reachable from the script.
- Add the following inside the `.bash_profile` file: `jump && exit`. This will execute on every user login
and when the user decides to exit, it will also exit the session on the jump server. 

Then you can create any user and have them use the jumpgate.

As an extra security step, add a user's own key (aka from their own laptop or pc or what have you) to the `authorized_keys`
file for their user on the jumpgate.

#### Todo:

- figure way to handle .env file after installation
- add to pypi for easy install

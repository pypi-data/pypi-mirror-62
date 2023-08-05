# Medium SDK for Python

This repository contains the open source SDK for integrating
[Medium](https://medium.com/)'s OAuth2 REST API with your Python app.

For full API documentation, see our [developer docs](https://github.com/Medium/medium-api-docs).

**Warning:** This is an unofficial project to integrate with Mediums API. This project is intended to maintain
work on the library after updates have ceased on a previous version. The author makes no claim to any of the
intellectual property herein, or any of the the trademarks owned or protected by Medium. 

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/Porter97/Python-Medium

Installers for the latest released version are available at the [Python
package index](https://pypi.org/project/Python-Medium)

```sh
# PyPI
pip install python-medium
```

## Installing dependencies

To install dependencies using pip:

```
pip install -r requirements.txt
```

## Usage

```python
from medium import Client

# Go to http://medium.com/me/applications to get your application_id and application_secret.
client = Client(application_id="MY_APPLICATION_ID", application_secret="MY_APPLICATION_SECRET")

# Build the URL where you can send the user to obtain an authorization code.
auth_url = client.get_authorization_url("secretstate", "https://yoursite.com/callback/medium",
                                        ["basicProfile", "publishPost"])

# (Send the user to the authorization URL to obtain an authorization code.)

# Exchange the authorization code for an access token.
auth = client.exchange_authorization_code("YOUR_AUTHORIZATION_CODE",
                                          "https://yoursite.com/callback/medium")

# The access token is automatically set on the client for you after
# a successful exchange, but if you already have a token, you can set it
# directly.
client.access_token = auth["access_token"]

# Get profile details of the user identified by the access token.
user = client.get_current_user()

# Create a draft post.
post = client.create_post(user_id=user["id"], title="Title", content="<h2>Title</h2><p>Content</p>",
                          content_format="html", publish_status="draft", publication_id="b45573563f5a",
                           notify_followers=True)

# List user publications
publications = client.list_publications(user_id=user["id"])

# Retrieve RSS feed of current user posts
feed = client.list_articles(user['username'])

# List publication contributors
pub_contributors = client.list_publications_contributors(publication_id=publications[0]["id"])

# When your access token expires, use the refresh token to get a new one.
client.exchange_refresh_token(auth["refresh_token"])

# Confirm everything went ok. post["url"] has the location of the created post.
print("My new post!", post["url"])
```

## Running tests

The testing module is currently under development, if you would like to contribute please
file a PR and I would be happy to merge it.

## Contributing

Questions, comments, bug reports, and pull requests are all welcomed.

## Authors

- [Kyle Hardgrave](https://github.com/kylehg) (Original Author)
- [Spencer Porter](https://github.com/porter97) (This Version)

## License

Copyright 2015 [A Medium Corporation](https://medium.com/)

Licensed under Apache License Version 2.0. Details in the attached LICENSE file.

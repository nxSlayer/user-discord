# Project README

This is a Python project that provides a `ClientDiscord` class for interacting with the Discord API and a `SocketDiscord` class for handling WebSocket events. It allows you to perform various actions such as logging in with a token, sending messages, deleting messages, retrieving DMs, managing servers and friends, retrieving channel messages, setting status and bio, and changing the user avatar.

## Requirements

- Python 3.x
- `requests` library
- `websocket-client` library

## Installation

1. ```shell
   pip install user-discord
   ```

## Usage

1. Create an instance of the `ClientDiscord` class:
   ```python
   client = ClientDiscord()
   ```

2. Log in to an account using a token:
   ```python
   token = "<YOUR_DISCORD_TOKEN>"
   client.login_token(token)
   ```

3. Use the available methods to interact with the Discord API. Here are some examples:
   - Sending a message to a channel:
     ```python
     channel_id = "<CHANNEL_ID>"
     message = "Hello, Discord!"
     client.send_message(channel_id, message)
     ```

   - Deleting a message in a channel:
     ```python
     channel_id = "<CHANNEL_ID>"
     message_id = "<MESSAGE_ID>"
     client.delete_message(channel_id, message_id)
     ```

   - Getting a list of users in DM:
     ```python
     dms = client.get_dms()
     ```

   - Getting a list of your servers:
     ```python
     servers = client.get_servers()
     ```

   - Getting a list of your friends:
     ```python
     friends = client.get_friends()
     ```

   - Getting a list of messages in a channel:
     ```python
     channel_id = "<CHANNEL_ID>"
     messages = client.get_channel_messages(channel_id)
     ```

   - Setting user status:
     ```python
     status = "<STATUS>"
     content = "<CUSTOM_STATUS_CONTENT>"
     emoji = "<CUSTOM_STATUS_EMOJI>"
     client.set_status(status, content, emoji)
     ```

   - Setting user bio:
     ```python
     bio = "<BIO>"
     client.set_bio(bio)
     ```

   - Changing the user avatar using a URL:
     ```python
     avatar_url = "<AVATAR_URL>"
     client.set_avatar(avatar_url)
     ```

5. To handle WebSocket events, create an instance of the `SocketDiscord` class and use the `on` decorator to register event handlers:
   ```python
   socket = SocketDiscord(client)

   @socket.on('MESSAGE_CREATE')
   def handle_message_create(message):
       print("New message received:")
       print(message)

   # Register more event handlers as needed

   # Start the WebSocket connection
   socket.start_ws()
   ```

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

# Conversation-Pyrogram
A conversation plugin class for pyrogram using inbuild Update Handlers

Complete list of handlers to be used without `Handlers` postfix :-
	https://docs.pyrogram.org/api/handlers#index

# Usage
```Python
listen = Conversation(client)
answer = listen.CallbackQuery(filters.user(update.from_user.id))
```

# Example
```Python
@app.on_message(filters.command('start'))
async def start(client, message):
	listen = Conversation(client)
	await client.send_mesage(messsage.chat.id, "What's your name?")
	reply_message = listen.Message(filters.chat(messsage.chat.id), timeout = None)
	if reply_message:
		reply_message.reply(f'hello {reply_message.text}')

```

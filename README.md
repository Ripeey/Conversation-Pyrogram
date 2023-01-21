# Conversation-Pyrogram
A conversation plugin class for pyrogram using inbuild Update Handlers

Complete list of handlers to be used without `Handlers` postfix :-
	https://docs.pyrogram.org/api/handlers#index

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install or simply copy the class file to your project.

```bash
pip install git+https://github.com/Ripeey/Conversation-Pyrogram
```

# Basic Usage
`main.py` Where the Client is initialized
```Python
from pyrogram import Client
from convopyro import Conversation

app = Client('MyApp')
Conversation(app) # That's it!
```
Then at any [update handler](https://docs.pyrogram.org/start/updates#using-decorators)
```Python
answer = client.listen.CallbackQuery(filters.user(update.from_user.id))
```

# Example

```python

from pyrogram       import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from convopyro import listen_message, stop_listen

@Client.on_message(filters.command(["start"], ["!",".","/"]) & filters.private)
async def start(client:Client, message:Message):
    await client.send_message(
        chat_id      = message.chat.id,
        text         = "What's your name?",
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Stop Listen", callback_data="stop_listen")]]
        )
    )

    answer = await listen_message(client, message.chat.id, timeout=None)
    if answer:
        await answer.reply(f"hello {answer.text}")
    else:
        await message.reply("Canceled Answer")

@Client.on_callback_query(filters.regex(pattern=r"^stop_listen$"))
async def listen_stopped(client:Client, callback_query:CallbackQuery):
    await stop_listen(client, callback_query.from_user.id)
    await callback_query.message.delete()

```

# Advanced Usage
The conversation class has 2 primary methods `listen.Handler` ([Handlers](https://docs.pyrogram.org/api/handlers#index) like **Message, CallbackQuery** ...etc) and `listen.Cancel` for ending an ongoing listener.

## listen.Handler()
The conversation `listen.Message` **(or any other [Handler](https://docs.pyrogram.org/api/handlers#index))** takes 3 parameters, default is `None` but either `filter` or `id` as parameter is required.

- **filters :** [Single](https://docs.pyrogram.org/topics/use-filters#single-filters) or [Combined](https://docs.pyrogram.org/topics/use-filters#combining-filters) is required but this is **optional** if `id` is passed with a valid single [user](https://docs.pyrogram.org/api/filters#pyrogram.filters.user) or [chat](https://docs.pyrogram.org/api/filters#pyrogram.filters.chat) filter (which will learn below).
- **id :** An unique id for each listen, this could be [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), a single [user filter](https://docs.pyrogram.org/api/filters#pyrogram.filters.user) or [chat filter](https://docs.pyrogram.org/api/filters#pyrogram.filters.chat), this is mostly **optional** and only needed to `Cancel()` a conversation listen. 
If **user/chat filter** is passed then it **combines** itself with `filters` so you dont need to repeat again in `filters` using `&`, where as if **str** is used it's just used normally as `id`.

- **timeout :** Waiting time in seconds [int](https://docs.python.org/3/library/functions.html#int) for getting a response **optional**.

#### Return
- **Update** :  Based on handlers used could be one of received updates such as [Message](https://docs.pyrogram.org/api/types/Message), [CallbackQuery](https://docs.pyrogram.org/api/types/CallbackQuery), etc.
- **None** : When listen gets cancel using `listen.Cancel` a None is return as response at listen callback.
- **Exception** : An `asyncio.TimeoutError` is raised if provided waiting time get's over.

## listen.Cancel()
The conversation `listen.Cancel` takes 1 required parameter. This method is used to cancel a specific conversation listen.

- **id** : An unique id provided during listen, this could be [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), a single [user filter](https://docs.pyrogram.org/api/filters#pyrogram.filters.user) or [chat filter](https://docs.pyrogram.org/api/filters#pyrogram.filters.chat).

#### Return
- **Boolean** :  False if `id` provided already cancelled or invalid.

# Example
```Python
@app.on_callback_query(filters.regex(r'stop'))
async def _(client, query):
	# This will return response None at listen
	await client.listen.Cancel(filters.user(query.from_user.id))

@app.on_message(filters.regex(r'hi'))
async def _(client, message):
	button = InlineKeyboardMarkup([[InlineKeyboardButton('Cancel Question', callback_data = 'stop')]])
	question = await client.send_message(message.chat.id, 'Enter your name in 5s.', reply_markup = button)
	# A nice flow of conversation
	try:
		response = await client.listen.Message(filters.text, id = filters.user(message.from_user.id), timeout = 5)
	except asyncio.TimeoutError:
		await message.reply('Too late 5s gone.')
	else:
		if response:
			await response.reply(f'Hello {response.text}')
		else:
			await message.reply('Okay cancelled question!')
	finally:
		await question.delete()
```

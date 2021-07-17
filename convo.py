#!/usr/bin/python3
from collections import OrderedDict
import pyrogram, asyncio

class Conversation():
	"""
	A conversation plugin class for pyrogram using inbuild Update Handlers.
	Complete list of handlers to be used without `Handlers` postfix :-
		https://docs.pyrogram.org/api/handlers#index

	Usage:
		listen = Conversation(client)
		answer = listen.CallbackQuery(filters.user(update.from.id))

	Example:
		@app.on_message(filters.command('start'))
		async def start(client, message):
			listen = Conversation(client)
			await client.send_mesage(messsage.chat.id, "What's your name?")
			reply_message = listen.Message(filters.chat(messsage.chat.id), timeout = None)
			if reply_message:
				reply_message.reply(f'hello {message.text}')
	"""
	def __init__(self, client : pyrogram.Client):
		self.client = client
		self.handlers = {}

	async def __add(self, hdlr, *args, timeout = None):
		async def dump(_, update): 
			await self.__remove(id(dump), update)
		
		group = -0x3e7
		handler = hdlr(dump, *args)
		event = asyncio.Event()
		
		if group not in self.client.dispatcher.groups:
			self.client.dispatcher.groups[group] = []
			self.client.dispatcher.groups = OrderedDict(sorted(self.client.dispatcher.groups.items()))

		app.dispatcher.groups[group].append(handler)
		self.handlers[id(dump)] = (handler, group, event)
		try:
			await asyncio.wait_for(event.wait(), timeout)
		except asyncio.exceptions.TimeoutError:
			await self.__remove(id(dump))
		
		return self.handlers.pop(id(dump))

	async def __remove(self, cid, update = None):
		handler, group, event = self.handlers[cid]
		self.client.dispatcher.groups[group].remove(handler)
		self.handlers[cid] = update
		event.set()

	def __getattr__(self, name):
		async def wrapper(*args, **kwargs):
			return await self.__add(getattr(pyrogram.handlers, f'{name}Handler'), *args, **kwargs)
		return wrapper

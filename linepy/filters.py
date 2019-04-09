class Filter:
    def __call__(self, message):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    def __call__(self, message):
        return not self.base(message)


class AndFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    def __call__(self, message):
        return self.base(message) and self.other(message)


class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    def __call__(self, message):
        return self.base(message) or self.other(message)


def create(name: str, func: callable, **kwargs) -> type:
	d = {"__call__": func}
	d.update(kwargs)
	return type(name, (Filter,), d)()

class Filters:

	create = create

	#content
	text = create("Text", lambda _,m: bool(m.contentType == 0))
	image = create("Image", lambda _,m: bool(m.contentType == 1))
	video = create("Video", lambda _,m: bool(m.contentType == 2))
	audio = create("Audio", lambda _,m: bool(m.contentType == 3))
	html = create("Html", lambda _,m: bool(m.contentType == 4))
	pdf = create("Pdf", lambda _,m: bool(m.contentType == 5))
	call = create("Call", lambda _,m: bool(m.contentType == 6))
	sticker = create("Sticker", lambda _,m: bool(m.contentType == 7))
	gift = create("Gift", lambda _,m: bool(m.contentType == 9))
	link = create("Link", lambda _,m: bool(m.contentType == 12))
	contact = create("Contact", lambda _,m: bool(m.contentType == 13))
	files = create("Files", lambda _,m: bool(m.contentType == 14))
	location = create("Location", lambda _,m: bool(m.contentType == 15))
	post = create("Post", lambda _,m: bool(m.contentType == 16))
	rich = create("Rich", lambda _,m: bool(m.contentType == 17))
	event = create("Event", lambda _,m: bool(m.contentType == 18))
	music = create("Music", lambda _,m: bool(m.contentType == 19))
	mention = create("Mention", lambda _,m: bool('MENTION' in m.contentMetadata.keys()))
	reply = create("Reply", lambda _,m: bool(m.contentMetadata["message_relation_type_code"] == "reply"))

	#Instance
	group = create("Group", lambda _,m: bool(m.toType == 2))
	private = create("Private", lambda _,m: bool(m.toType == 0))
	both = create("Both", lambda _,m: bool(m.toType in [0, 2, 1]))

	#update group
	update_name = create("UpdateName", lambda _,m: bool(m.param3 == '1'))
	update_image = create("UpdateImage", lambda _,m: bool(m.param3 == '2'))
	update_qr = create("UpdateQr", lambda _,m: bool(m.param3 == '4'))
	update_all = create("UpdateAll", lambda _,m: bool(m.param3 in ["1", "2", "4"]))

	@staticmethod
	def command(commands: str or list,
					prefix: str or list = "/",
					separator: str = " ",
					case_sensitive: bool = True):
		def f(_, m):
			m.command = False
			if m.text:
				for i in _.p:
					if m.text.startswith(i):
						t = m.text.split(_.s)
						c, a = t[0][len(i):], t[1:]
						c = c if _.cs else c.lower()
						m.command = ([c] + a) if c in _.c else None						
			return bool(m.command)
		return create(
		"Command",
		f,
		c = {commands if case_sensitive
				else commands.lower()}
		if not isinstance(commands, list)
		else {c if case_sensitive
				else c.lower()
				for c in commands},
		p=set(prefix) if prefix else {""},
		s=separator,
		cs=case_sensitive
		)

	class user(Filter, set):
		def __init__(self, users: int or str or list = None):
			users = [] if users is None else users if isinstance(user, list) else [users]
			super().__init__(
				{"me" if i in ["me", "self"] else i.lower() if isinstance(i, str)  else i for i in users}
				if isinstance(i, list) else
				{"me" if users in ["me", "self"] else users.lower() if isinstance(i, str) else user}
			)

		def __call__(self, message):
			return bool(
				message._from
				and (message._from in self
					or ("me" in self)
				)
			)

	class chat(Filter, set):
		def __init__(self, chats: int or str or list = None):
			chats = [] if chats is None else chats if isinstance(chats, list) else [chats]
			super().__init__(
                {i.lower() if isinstance(i, str)  else i for i in chats}
                if isinstance(chats, list) else
                {chats.lower() if isinstance(chats, str) else chats}
            )
		def __call__(self, message):
			return bool(
				message.toType == 2
				and (message.to in self)
			)

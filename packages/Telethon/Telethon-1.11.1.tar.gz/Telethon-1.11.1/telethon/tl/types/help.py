"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from typing import Optional, List, Union, TYPE_CHECKING
import os
import struct
from datetime import datetime
if TYPE_CHECKING:
    from ...tl.types import TypeAccessPointRule, TypeChat, TypeDataJSON, TypeDocument, TypeMessageEntity, TypePeer, TypeRecentMeUrl, TypeUser
    from ...tl.types.help import TypeTermsOfService



class AppUpdate(TLObject):
    CONSTRUCTOR_ID = 0x1da7158f
    SUBCLASS_OF_ID = 0x5897069e

    # noinspection PyShadowingBuiltins
    def __init__(self, id: int, version: str, text: str, entities: List['TypeMessageEntity'], can_not_skip: Optional[bool]=None, document: Optional['TypeDocument']=None, url: Optional[str]=None):
        """
        Constructor for help.AppUpdate: Instance of either AppUpdate, NoAppUpdate.
        """
        self.id = id
        self.version = version
        self.text = text
        self.entities = entities
        self.can_not_skip = can_not_skip
        self.document = document
        self.url = url

    def to_dict(self):
        return {
            '_': 'AppUpdate',
            'id': self.id,
            'version': self.version,
            'text': self.text,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.entities],
            'can_not_skip': self.can_not_skip,
            'document': self.document.to_dict() if isinstance(self.document, TLObject) else self.document,
            'url': self.url
        }

    def __bytes__(self):
        return b''.join((
            b'\x8f\x15\xa7\x1d',
            struct.pack('<I', (0 if self.can_not_skip is None or self.can_not_skip is False else 1) | (0 if self.document is None or self.document is False else 2) | (0 if self.url is None or self.url is False else 4)),
            struct.pack('<i', self.id),
            self.serialize_bytes(self.version),
            self.serialize_bytes(self.text),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.entities)),b''.join(bytes(x) for x in self.entities),
            b'' if self.document is None or self.document is False else (bytes(self.document)),
            b'' if self.url is None or self.url is False else (self.serialize_bytes(self.url)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _can_not_skip = bool(flags & 1)
        _id = reader.read_int()
        _version = reader.tgread_string()
        _text = reader.tgread_string()
        reader.read_int()
        _entities = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _entities.append(_x)

        if flags & 2:
            _document = reader.tgread_object()
        else:
            _document = None
        if flags & 4:
            _url = reader.tgread_string()
        else:
            _url = None
        return cls(id=_id, version=_version, text=_text, entities=_entities, can_not_skip=_can_not_skip, document=_document, url=_url)


class ConfigSimple(TLObject):
    CONSTRUCTOR_ID = 0x5a592a6c
    SUBCLASS_OF_ID = 0x29183ac4

    def __init__(self, date: Optional[datetime], expires: Optional[datetime], rules: List['TypeAccessPointRule']):
        """
        Constructor for help.ConfigSimple: Instance of ConfigSimple.
        """
        self.date = date
        self.expires = expires
        self.rules = rules

    def to_dict(self):
        return {
            '_': 'ConfigSimple',
            'date': self.date,
            'expires': self.expires,
            'rules': [] if self.rules is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.rules]
        }

    def __bytes__(self):
        return b''.join((
            b'l*YZ',
            self.serialize_datetime(self.date),
            self.serialize_datetime(self.expires),
            struct.pack('<i', len(self.rules)),b''.join(bytes(x) for x in self.rules),
        ))

    @classmethod
    def from_reader(cls, reader):
        _date = reader.tgread_date()
        _expires = reader.tgread_date()
        _rules = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _rules.append(_x)

        return cls(date=_date, expires=_expires, rules=_rules)


class DeepLinkInfo(TLObject):
    CONSTRUCTOR_ID = 0x6a4ee832
    SUBCLASS_OF_ID = 0x984aac38

    def __init__(self, message: str, update_app: Optional[bool]=None, entities: Optional[List['TypeMessageEntity']]=None):
        """
        Constructor for help.DeepLinkInfo: Instance of either DeepLinkInfoEmpty, DeepLinkInfo.
        """
        self.message = message
        self.update_app = update_app
        self.entities = entities

    def to_dict(self):
        return {
            '_': 'DeepLinkInfo',
            'message': self.message,
            'update_app': self.update_app,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.entities]
        }

    def __bytes__(self):
        return b''.join((
            b'2\xe8Nj',
            struct.pack('<I', (0 if self.update_app is None or self.update_app is False else 1) | (0 if self.entities is None or self.entities is False else 2)),
            self.serialize_bytes(self.message),
            b'' if self.entities is None or self.entities is False else b''.join((b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.entities)),b''.join(bytes(x) for x in self.entities))),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _update_app = bool(flags & 1)
        _message = reader.tgread_string()
        if flags & 2:
            reader.read_int()
            _entities = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _entities.append(_x)

        else:
            _entities = None
        return cls(message=_message, update_app=_update_app, entities=_entities)


class DeepLinkInfoEmpty(TLObject):
    CONSTRUCTOR_ID = 0x66afa166
    SUBCLASS_OF_ID = 0x984aac38

    def to_dict(self):
        return {
            '_': 'DeepLinkInfoEmpty'
        }

    def __bytes__(self):
        return b''.join((
            b'f\xa1\xaff',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class InviteText(TLObject):
    CONSTRUCTOR_ID = 0x18cb9f78
    SUBCLASS_OF_ID = 0xcf70aa35

    def __init__(self, message: str):
        """
        Constructor for help.InviteText: Instance of InviteText.
        """
        self.message = message

    def to_dict(self):
        return {
            '_': 'InviteText',
            'message': self.message
        }

    def __bytes__(self):
        return b''.join((
            b'x\x9f\xcb\x18',
            self.serialize_bytes(self.message),
        ))

    @classmethod
    def from_reader(cls, reader):
        _message = reader.tgread_string()
        return cls(message=_message)


class NoAppUpdate(TLObject):
    CONSTRUCTOR_ID = 0xc45a6536
    SUBCLASS_OF_ID = 0x5897069e

    def to_dict(self):
        return {
            '_': 'NoAppUpdate'
        }

    def __bytes__(self):
        return b''.join((
            b'6eZ\xc4',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class PassportConfig(TLObject):
    CONSTRUCTOR_ID = 0xa098d6af
    SUBCLASS_OF_ID = 0xc666c0ad

    # noinspection PyShadowingBuiltins
    def __init__(self, hash: int, countries_langs: 'TypeDataJSON'):
        """
        Constructor for help.PassportConfig: Instance of either PassportConfigNotModified, PassportConfig.
        """
        self.hash = hash
        self.countries_langs = countries_langs

    def to_dict(self):
        return {
            '_': 'PassportConfig',
            'hash': self.hash,
            'countries_langs': self.countries_langs.to_dict() if isinstance(self.countries_langs, TLObject) else self.countries_langs
        }

    def __bytes__(self):
        return b''.join((
            b'\xaf\xd6\x98\xa0',
            struct.pack('<i', self.hash),
            bytes(self.countries_langs),
        ))

    @classmethod
    def from_reader(cls, reader):
        _hash = reader.read_int()
        _countries_langs = reader.tgread_object()
        return cls(hash=_hash, countries_langs=_countries_langs)


class PassportConfigNotModified(TLObject):
    CONSTRUCTOR_ID = 0xbfb9f457
    SUBCLASS_OF_ID = 0xc666c0ad

    def to_dict(self):
        return {
            '_': 'PassportConfigNotModified'
        }

    def __bytes__(self):
        return b''.join((
            b'W\xf4\xb9\xbf',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class ProxyDataEmpty(TLObject):
    CONSTRUCTOR_ID = 0xe09e1fb8
    SUBCLASS_OF_ID = 0x21e2a448

    def __init__(self, expires: Optional[datetime]):
        """
        Constructor for help.ProxyData: Instance of either ProxyDataEmpty, ProxyDataPromo.
        """
        self.expires = expires

    def to_dict(self):
        return {
            '_': 'ProxyDataEmpty',
            'expires': self.expires
        }

    def __bytes__(self):
        return b''.join((
            b'\xb8\x1f\x9e\xe0',
            self.serialize_datetime(self.expires),
        ))

    @classmethod
    def from_reader(cls, reader):
        _expires = reader.tgread_date()
        return cls(expires=_expires)


class ProxyDataPromo(TLObject):
    CONSTRUCTOR_ID = 0x2bf7ee23
    SUBCLASS_OF_ID = 0x21e2a448

    def __init__(self, expires: Optional[datetime], peer: 'TypePeer', chats: List['TypeChat'], users: List['TypeUser']):
        """
        Constructor for help.ProxyData: Instance of either ProxyDataEmpty, ProxyDataPromo.
        """
        self.expires = expires
        self.peer = peer
        self.chats = chats
        self.users = users

    def to_dict(self):
        return {
            '_': 'ProxyDataPromo',
            'expires': self.expires,
            'peer': self.peer.to_dict() if isinstance(self.peer, TLObject) else self.peer,
            'chats': [] if self.chats is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.chats],
            'users': [] if self.users is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.users]
        }

    def __bytes__(self):
        return b''.join((
            b'#\xee\xf7+',
            self.serialize_datetime(self.expires),
            bytes(self.peer),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.chats)),b''.join(bytes(x) for x in self.chats),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.users)),b''.join(bytes(x) for x in self.users),
        ))

    @classmethod
    def from_reader(cls, reader):
        _expires = reader.tgread_date()
        _peer = reader.tgread_object()
        reader.read_int()
        _chats = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _chats.append(_x)

        reader.read_int()
        _users = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _users.append(_x)

        return cls(expires=_expires, peer=_peer, chats=_chats, users=_users)


class RecentMeUrls(TLObject):
    CONSTRUCTOR_ID = 0xe0310d7
    SUBCLASS_OF_ID = 0xf269c477

    def __init__(self, urls: List['TypeRecentMeUrl'], chats: List['TypeChat'], users: List['TypeUser']):
        """
        Constructor for help.RecentMeUrls: Instance of RecentMeUrls.
        """
        self.urls = urls
        self.chats = chats
        self.users = users

    def to_dict(self):
        return {
            '_': 'RecentMeUrls',
            'urls': [] if self.urls is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.urls],
            'chats': [] if self.chats is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.chats],
            'users': [] if self.users is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.users]
        }

    def __bytes__(self):
        return b''.join((
            b'\xd7\x10\x03\x0e',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.urls)),b''.join(bytes(x) for x in self.urls),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.chats)),b''.join(bytes(x) for x in self.chats),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.users)),b''.join(bytes(x) for x in self.users),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _urls = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _urls.append(_x)

        reader.read_int()
        _chats = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _chats.append(_x)

        reader.read_int()
        _users = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _users.append(_x)

        return cls(urls=_urls, chats=_chats, users=_users)


class Support(TLObject):
    CONSTRUCTOR_ID = 0x17c6b5f6
    SUBCLASS_OF_ID = 0x7159bceb

    def __init__(self, phone_number: str, user: 'TypeUser'):
        """
        Constructor for help.Support: Instance of Support.
        """
        self.phone_number = phone_number
        self.user = user

    def to_dict(self):
        return {
            '_': 'Support',
            'phone_number': self.phone_number,
            'user': self.user.to_dict() if isinstance(self.user, TLObject) else self.user
        }

    def __bytes__(self):
        return b''.join((
            b'\xf6\xb5\xc6\x17',
            self.serialize_bytes(self.phone_number),
            bytes(self.user),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _user = reader.tgread_object()
        return cls(phone_number=_phone_number, user=_user)


class SupportName(TLObject):
    CONSTRUCTOR_ID = 0x8c05f1c9
    SUBCLASS_OF_ID = 0x7f50b7c2

    def __init__(self, name: str):
        """
        Constructor for help.SupportName: Instance of SupportName.
        """
        self.name = name

    def to_dict(self):
        return {
            '_': 'SupportName',
            'name': self.name
        }

    def __bytes__(self):
        return b''.join((
            b'\xc9\xf1\x05\x8c',
            self.serialize_bytes(self.name),
        ))

    @classmethod
    def from_reader(cls, reader):
        _name = reader.tgread_string()
        return cls(name=_name)


class TermsOfService(TLObject):
    CONSTRUCTOR_ID = 0x780a0310
    SUBCLASS_OF_ID = 0x20ee8312

    # noinspection PyShadowingBuiltins
    def __init__(self, id: 'TypeDataJSON', text: str, entities: List['TypeMessageEntity'], popup: Optional[bool]=None, min_age_confirm: Optional[int]=None):
        """
        Constructor for help.TermsOfService: Instance of TermsOfService.
        """
        self.id = id
        self.text = text
        self.entities = entities
        self.popup = popup
        self.min_age_confirm = min_age_confirm

    def to_dict(self):
        return {
            '_': 'TermsOfService',
            'id': self.id.to_dict() if isinstance(self.id, TLObject) else self.id,
            'text': self.text,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.entities],
            'popup': self.popup,
            'min_age_confirm': self.min_age_confirm
        }

    def __bytes__(self):
        return b''.join((
            b'\x10\x03\nx',
            struct.pack('<I', (0 if self.popup is None or self.popup is False else 1) | (0 if self.min_age_confirm is None or self.min_age_confirm is False else 2)),
            bytes(self.id),
            self.serialize_bytes(self.text),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.entities)),b''.join(bytes(x) for x in self.entities),
            b'' if self.min_age_confirm is None or self.min_age_confirm is False else (struct.pack('<i', self.min_age_confirm)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _popup = bool(flags & 1)
        _id = reader.tgread_object()
        _text = reader.tgread_string()
        reader.read_int()
        _entities = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _entities.append(_x)

        if flags & 2:
            _min_age_confirm = reader.read_int()
        else:
            _min_age_confirm = None
        return cls(id=_id, text=_text, entities=_entities, popup=_popup, min_age_confirm=_min_age_confirm)


class TermsOfServiceUpdate(TLObject):
    CONSTRUCTOR_ID = 0x28ecf961
    SUBCLASS_OF_ID = 0x293c2977

    def __init__(self, expires: Optional[datetime], terms_of_service: 'TypeTermsOfService'):
        """
        Constructor for help.TermsOfServiceUpdate: Instance of either TermsOfServiceUpdateEmpty, TermsOfServiceUpdate.
        """
        self.expires = expires
        self.terms_of_service = terms_of_service

    def to_dict(self):
        return {
            '_': 'TermsOfServiceUpdate',
            'expires': self.expires,
            'terms_of_service': self.terms_of_service.to_dict() if isinstance(self.terms_of_service, TLObject) else self.terms_of_service
        }

    def __bytes__(self):
        return b''.join((
            b'a\xf9\xec(',
            self.serialize_datetime(self.expires),
            bytes(self.terms_of_service),
        ))

    @classmethod
    def from_reader(cls, reader):
        _expires = reader.tgread_date()
        _terms_of_service = reader.tgread_object()
        return cls(expires=_expires, terms_of_service=_terms_of_service)


class TermsOfServiceUpdateEmpty(TLObject):
    CONSTRUCTOR_ID = 0xe3309f7f
    SUBCLASS_OF_ID = 0x293c2977

    def __init__(self, expires: Optional[datetime]):
        """
        Constructor for help.TermsOfServiceUpdate: Instance of either TermsOfServiceUpdateEmpty, TermsOfServiceUpdate.
        """
        self.expires = expires

    def to_dict(self):
        return {
            '_': 'TermsOfServiceUpdateEmpty',
            'expires': self.expires
        }

    def __bytes__(self):
        return b''.join((
            b'\x7f\x9f0\xe3',
            self.serialize_datetime(self.expires),
        ))

    @classmethod
    def from_reader(cls, reader):
        _expires = reader.tgread_date()
        return cls(expires=_expires)


class UserInfo(TLObject):
    CONSTRUCTOR_ID = 0x1eb3758
    SUBCLASS_OF_ID = 0x5c53d7d8

    def __init__(self, message: str, entities: List['TypeMessageEntity'], author: str, date: Optional[datetime]):
        """
        Constructor for help.UserInfo: Instance of either UserInfoEmpty, UserInfo.
        """
        self.message = message
        self.entities = entities
        self.author = author
        self.date = date

    def to_dict(self):
        return {
            '_': 'UserInfo',
            'message': self.message,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.entities],
            'author': self.author,
            'date': self.date
        }

    def __bytes__(self):
        return b''.join((
            b'X7\xeb\x01',
            self.serialize_bytes(self.message),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.entities)),b''.join(bytes(x) for x in self.entities),
            self.serialize_bytes(self.author),
            self.serialize_datetime(self.date),
        ))

    @classmethod
    def from_reader(cls, reader):
        _message = reader.tgread_string()
        reader.read_int()
        _entities = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _entities.append(_x)

        _author = reader.tgread_string()
        _date = reader.tgread_date()
        return cls(message=_message, entities=_entities, author=_author, date=_date)


class UserInfoEmpty(TLObject):
    CONSTRUCTOR_ID = 0xf3ae2eed
    SUBCLASS_OF_ID = 0x5c53d7d8

    def to_dict(self):
        return {
            '_': 'UserInfoEmpty'
        }

    def __bytes__(self):
        return b''.join((
            b'\xed.\xae\xf3',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


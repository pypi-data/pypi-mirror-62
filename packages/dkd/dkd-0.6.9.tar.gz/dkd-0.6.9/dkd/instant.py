# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import time as time_lib
import weakref

from .envelope import Envelope
from .content import Content
from .message import Message
from .secure import SecureMessage


class InstantMessage(Message):
    """
        Instant Message
        ~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content
            content  : {...}
        }
    """

    def __new__(cls, msg: dict):
        """
        Create instant message

        :param msg: message info
        :return: InstantMessage object
        """
        if msg is None:
            return None
        elif cls is InstantMessage:
            if isinstance(msg, InstantMessage):
                # return InstantMessage object directly
                return msg
        # new InstantMessage(dict)
        return super().__new__(cls, msg)

    def __init__(self, msg: dict):
        if self is msg:
            # no need to init again
            return
        super().__init__(msg)
        self.__delegate: weakref.ReferenceType = None
        # lazy
        self.__content: Content = None

    @property
    def delegate(self):  # Optional[InstantMessageDelegate]
        if self.__delegate is not None:
            return self.__delegate()

    @delegate.setter
    def delegate(self, value):
        if value is None:
            self.__delegate = None
        else:
            self.__delegate = weakref.ref(value)

    @property
    def content(self) -> Content:
        if self.__content is None:
            self.__content = Content(self['content'])
        return self.__content

    """
        Encrypt the Instant Message to Secure Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |
            | content  |      | data     |  1. data = encrypt(content, PW)
            +----------+      | key/keys |  2. key  = encrypt(PW, receiver.PK)
                              +----------+
    """

    def encrypt(self, password: dict, members: list=None) -> SecureMessage:
        """
        Encrypt message content with password(symmetric key)

        :param password: A symmetric key for encrypting message content
        :param members:  If this is a group message, get all members here
        :return: SecureMessage object
        """
        # 0. check attachment for File/Image/Audio/Video message content
        #    (do it in 'core' module)
        msg = self.copy()

        # 1. encrypt 'message.content' to 'message.data'
        # 1.1. encrypt message content with password
        data = self.delegate.encrypt_content(content=self.content, key=password, msg=self)
        assert data is not None, 'failed to encrypt content with key: %s' % password
        # 1.2. encode encrypted data
        # 1.3. replace 'content' with encrypted 'data'
        msg['data'] = self.delegate.encode_data(data=data, msg=self)
        msg.pop('content')  # remove 'content'

        # 2. encrypt symmetric key(password) to 'key'/'keys'
        if members is None:
            # personal message
            key = self.delegate.encrypt_key(key=password, receiver=self.envelope.receiver, msg=self)
            if key is not None:
                base64 = self.delegate.encode_key(key=key, msg=self)
                assert base64 is not None, 'failed to encode key data: %s' % key
                msg['key'] = base64
        else:
            # group message
            keys = {}
            for member in members:
                # 2.1. serialize & encrypt symmetric key
                key = self.delegate.encrypt_key(key=password, receiver=member, msg=self)
                if key is not None:
                    # 2.2. encode encrypted key data
                    base64 = self.delegate.encode_key(key=key, msg=self)
                    assert base64 is not None, 'failed to encode key data: %s' % key
                    # 2.3. insert to 'message.keys' with member ID
                    keys[member] = base64
            if len(keys) > 0:
                msg['keys'] = keys
            # group ID
            group = self.content.group
            assert group is not None, 'group message content error: %s' % self
            # NOTICE: this help the receiver knows the group ID
            #         when the group message separated to multi-messages,
            #         if don't want the others know you are the group members,
            #         remove it.
            msg['group'] = group

        # 3. pack message
        return SecureMessage(msg)

    #
    #  Factory
    #
    @classmethod
    def new(cls, content: Content, envelope: Envelope=None,
            sender: str=None, receiver: str=None, time: int=0):
        if envelope:
            # share the same dictionary with envelope object
            msg = envelope.dictionary
            msg['content'] = content
        else:
            assert sender is not None and receiver is not None, 'sender/receiver error'
            if time == 0:
                time = int(time_lib.time())
            # build instant message info
            msg = {
                'sender': sender,
                'receiver': receiver,
                'time': time,
                'content': content,
            }
        return cls(msg)

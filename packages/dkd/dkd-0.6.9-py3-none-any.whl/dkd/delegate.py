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

from abc import ABC, abstractmethod
from typing import Optional

from .content import Content
from .instant import InstantMessage
from .secure import SecureMessage
from .reliable import ReliableMessage


#
#  Message Delegates
#

class InstantMessageDelegate(ABC):

    @abstractmethod
    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        """
        Encrypt 'message.content' to 'message.data' with symmetric key

        :param content: message content
        :param key:     symmetric key
        :param msg:     instant message
        :return:        encrypted message content data
        """
        raise NotImplemented

    @abstractmethod
    def encode_data(self, data: bytes, msg: InstantMessage) -> str:
        """
        Encode 'message.data' to String(Base64)

        :param data: encrypted content data
        :param msg:  instant message
        :return:     string
        """
        raise NotImplemented

    @abstractmethod
    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> Optional[bytes]:
        """
        Encrypt 'message.key' with receiver's public key (broadcast message has no key)

        :param key:      symmetric key to be encrypted
        :param receiver: receiver ID/string
        :param msg:      instant message
        :return:         encrypted key data
        """
        raise NotImplemented

    @abstractmethod
    def encode_key(self, key: bytes, msg: InstantMessage) -> Optional[str]:
        """
        Encode 'message.key' to String(Base64) (broadcast message has no key)

        :param key: encrypted key data
        :param msg: instant message
        :return:    string
        """
        raise NotImplemented


class SecureMessageDelegate(ABC):

    @abstractmethod
    def decode_key(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        """
        Decode 'message.key' to encrypted symmetric key data

        :param key: base64 string
        :param msg: secure message
        :return:    encrypted symmetric key data
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        """
        Decrypt 'message.key' with receiver's private key

        :param key:      encrypted symmetric key data
        :param sender:   sender/member ID string
        :param receiver: receiver/group ID string
        :param msg:      secure message
        :return:         symmetric key
        """
        raise NotImplemented

    @abstractmethod
    def decode_data(self, data: str, msg: SecureMessage) -> Optional[bytes]:
        """
        Decode 'message.data' to encrypted content data

        :param data: base64 string
        :param msg:  secure message
        :return:     encrypted content data
        """
        raise NotImplemented

    @abstractmethod
    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[Content]:
        """
        Decrypt 'message.data' with symmetric key

        :param data: encrypted content data
        :param key:  symmetric key
        :param msg:  secure message
        :return:     message content
        """
        raise NotImplemented

    @abstractmethod
    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        """
        Sign 'message.data' with sender's private key

        :param data:   encrypted message data
        :param sender: sender ID string
        :param msg:    secure message
        :return:       signature of encrypted message data
        """
        raise NotImplemented

    @abstractmethod
    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        """
        Encode 'message.signature' to String(Base64)

        :param signature: signature of message.data
        :param msg:       secure message
        :return:          string
        """
        raise NotImplemented


class ReliableMessageDelegate(SecureMessageDelegate):

    @abstractmethod
    def decode_signature(self, signature: str, msg: ReliableMessage) -> Optional[bytes]:
        """
        Decode 'message.signature' from String(Base64)

        :param signature: base64 string
        :param msg:       reliable message
        :return:          signature data
        """
        raise NotImplemented

    @abstractmethod
    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        """
        Verify the message data and signature with sender's public key

        :param data:      message content(encrypted) data
        :param signature: signature of message content(encrypted) data
        :param sender:    sender ID/string
        :param msg:       reliable message
        :return:          True on signature matched
        """
        raise NotImplemented

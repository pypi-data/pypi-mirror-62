# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import pytest
import socket
from blynklib import Connection, BlynkError, RedirectError


class TestBlynkConnection:
    @pytest.fixture
    def cb(self):
        connection = Connection('1234', log=print)
        yield connection

    def test_send(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.send', return_value=5)
        result = cb.send('1234')
        assert result == 5

    def test_send_ioerror(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.send', side_effect=IOError('IO'))
        result = cb.send('1234')
        assert result is None

    def test_send_oserror(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.send', side_effect=OSError('OS'))
        result = cb.send('1234')
        assert result is None

    def test_send_socket_timeout(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.send', side_effect=socket.timeout())
        result = cb.send('1234')
        assert result is None

    def test_send_error_retry_count(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.send', side_effect=OSError('OS'))
        mocker.spy(time, 'sleep')
        cb.send('1234')
        assert cb._socket.send.call_count == 3

    def test_receive(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.recv', return_value=b'12345')
        result = cb.receive(10, 1)
        assert result == b'12345'

    def test_receive_timeout(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.recv', side_effect=OSError('timed out'))
        result = cb.receive(10, 1)
        assert result == b''

    def test_receive_timeout_2(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.recv', side_effect=socket.timeout('timed out'))
        result = cb.receive(10, 1)
        assert result == b''

    def test_receive_eagain(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.recv', side_effect=IOError('[Errno 11]'))
        result = cb.receive(10, 1)
        assert result == b''

    def test_receive_etimeout(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.recv', side_effect=OSError('[Errno 60]'))
        result = cb.receive(10, 1)
        assert result == b''

    def test_receive_raise_other_oserror(self, cb, mocker):
        cb._socket = socket.socket()
        mocker.patch('socket.socket.recv', side_effect=OSError('[Errno 13]'))
        with pytest.raises(OSError) as os_err:
            cb.receive(10, 1)
        assert '[Errno 13]' in str(os_err.value)

    def test_is_server_alive_negative(self, cb):
        result = cb.is_server_alive()
        assert result is False

    def test_is_server_alive_positive_ping(self, cb, mocker):
        cb._last_rcv_time = int(time.time() * 1000)
        mocker.patch.object(cb, 'send', return_value=None)
        result = cb.is_server_alive()
        assert result is True

    def test_is_server_alive_positive_no_ping_1(self, cb):
        cb._last_rcv_time = int(time.time() * 1000)
        cb._last_ping_time = int(time.time() * 1000)
        result = cb.is_server_alive()
        assert result is True

    def test_is_server_alive_positive_no_ping_2(self, cb):
        cb._last_rcv_time = int(time.time() * 1000)
        cb._last_send_time = int(time.time() * 1000)
        result = cb.is_server_alive()
        assert result is True

    def test_get_socket(self, cb, mocker):
        mocker.patch('socket.socket')
        mocker.patch('socket.getaddrinfo')
        cb._get_socket()
        assert cb._state == cb.CONNECTING

    def test_get_socket_exception(self, cb, mocker):
        mocker.patch('socket.socket')
        mocker.patch('socket.getaddrinfo', side_effect=BlynkError('BE'))
        with pytest.raises(BlynkError) as b_err:
            cb._get_socket()
        assert 'Connection with the Blynk server failed: BE' in str(b_err.value)

    def test_authenticate(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=b'\x00\x00\x02\x00\xc8')
        cb._authenticate()
        assert cb._state == cb.AUTHENTICATED

    def test_authenticate_invalid_auth_token(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=b'\x00\x00\x02\x00\x09')
        with pytest.raises(BlynkError) as b_err:
            cb._authenticate()
            assert 'Invalid Auth Token' in str(b_err.value)

    def test_authenticate_redirect_message(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=b'\x29\x00\x02\x00\x11127.0.0.1\x004444')
        with pytest.raises(RedirectError) as r_err:
            cb._authenticate()
            # pytest exception wraps real exception - so we need access value field first
            assert '127.0.0.1' in r_err.value.server
            assert '4444' in r_err.value.port

    def test_authenticate_not_ok_status(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=b'\x00\x00\x02\x00\x19')
        with pytest.raises(BlynkError) as b_err:
            cb._authenticate()
            assert 'Auth stage failed. Status=25' in str(b_err.value)

    def test_authenticate_timeout(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=None)
        with pytest.raises(BlynkError) as b_err:
            cb._authenticate()
            assert 'Auth stage timeout' in str(b_err.value)

    def test_set_heartbeat_timeout(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=None)
        with pytest.raises(BlynkError) as b_err:
            cb._set_heartbeat()
            assert 'Heartbeat stage timeout' in str(b_err.value)

    def test_set_heartbeat_error_status(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=b'\x00\x00\x02\x00\x0e')
        with pytest.raises(BlynkError) as b_err:
            cb._set_heartbeat()
            assert 'Set heartbeat returned code=14' in str(b_err.value)

    def test_set_heartbeat_positive(self, cb, mocker):
        mocker.patch.object(cb, 'send', return_value=None)
        mocker.patch.object(cb, 'receive', return_value=b'\x00\x00\x02\x00\xc8')
        cb._set_heartbeat()

    def test_connected_false(self, cb):
        result = cb.connected()
        assert result is False

    def test_connected_true(self, cb):
        cb._state = cb.AUTHENTICATED
        result = cb.connected()
        assert result is True

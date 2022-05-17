#!/usr/bin/python3

# MIT License
#
# (C) Copyright [2020-2022] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# pylint: disable=missing-docstring

import unittest
import os
import io
from datetime import datetime, timezone, timedelta
import json
import uuid
import werkzeug
import flask
from swagger_server.uan_lib.uas_mgr import UanManager


app = flask.Flask(__name__)  # pylint: disable=invalid-name


class TestUanMgr(unittest.TestCase):
    """Tester for the UanMgr Class

    """
    os.environ["KUBERNETES_SERVICE_PORT"] = "443"
    os.environ["KUBERNETES_SERVICE_HOST"] = "127.0.0.1"
    public_key_str = (
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzpYg4QF8sj479"
        "cBdhLf6qyZPSueaQ9T7r96ejD7TUpwrjDxZFneZGm6dbFIRBR1P5"
        "/0TYbGBWvvHGZvunsp+wjVx6MlpUmaC4oQlPS9Re01NI60zI6den"
        "RofAGa2hlCRq6CtEX7IG2r8uKJa7intjQmyeUKCju6HKjZbamYBx"
        "7kxSdaKbsIzwwURL7g7od6dVh+R3XaFHLDWbS52wwsD09T4mIiUB"
        "O3wvs/ShApFsUmuG1DFgUfdCV+m2S67gr2VDUwmeZeV7mPDZRmCS"
        "UNCTuRM5RNjYBtaRPb6POl/wDKQQz3Q0hdlzg0jxiID//C3BASfK"
        "9i+UNWq7o3BSHNSj test-user@host.mydomain.com"
    )
    public_key = io.BytesIO()
    public_key.write(
        bytes(public_key_str, encoding='utf8')
    )
    with app.test_request_context('/'):
        uan_mgr = UanManager()

    # pylint: disable=missing-docstring,no-self-use
    def test_uan_mgr_init(self):
        return


if __name__ == '__main__':
    unittest.main()

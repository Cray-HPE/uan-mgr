#!/usr/bin/python3
# MIT License
#
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
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

import os
import unittest
import requests_mock
from swagger_server.uan_lib.uan_cfg import UanCfg


# pylint: disable=too-many-public-methods
@requests_mock.Mocker()
class TestUanCfg(unittest.TestCase):
    """Tester for the UanCfg class

    """
    uan_cfg = UanCfg(uan_cfg='swagger_server/test/cray-uan-mgr.yaml')
    uan_cfg_empty = UanCfg(
        uan_cfg='swagger_server/test/cray-uan-mgr-empty.yaml'
    )
    uan_cfg_svc = UanCfg(uan_cfg='swagger_server/test/cray-uan-mgr-svc.yaml')
    uan_cfg_svc_customer_access = UanCfg(
        uan_cfg='swagger_server/test/cray-uan-mgr-svc-customer-access.yaml'
    )

    # pylint: disable=missing-docstring,unused-argument
    def test_get_config(self, mocker):
        # Just make sure calling get_config() doesn't die on all the
        # configs...
        _ = self.uan_cfg.get_config()
        _ = self.uan_cfg_empty.get_config()
        _ = self.uan_cfg_svc.get_config()

#    @staticmethod
#    # pylint: disable=missing-docstring
#    def __load_bican_cases():
#        require_bican = os.environ.get('REQUIRE_BICAN', "false").lower()
#        expected_key = (
#            'expected_pool_soft' if  require_bican == "false"
#            else 'expected_pool_hard'
#        )
#        bican_cases = "swagger_server/test/bican_cases.yaml"
#        with open(bican_cases, 'r', encoding='utf-8') as infile:
#            cases = yaml.load(infile, Loader=yaml.FullLoader)['bican_cases']
#        return [
#            (
#                case[expected_key],
#                case['expected_subdomain'],
#                case['networks']
#            )
#            for case in cases
#        ]

#    # pylint: disable=missing-docstring
#    def __get_service_types_bican(self, mocker):
#        bican_cases = self.__load_bican_cases()
#        self.assertTrue(bican_cases) # not empty or None to be sure test is run
#        self.__reset_runtime_config(self.uan_cfg_svc_customer_access)
#        for expected_pool, expected_subdomain, networks in bican_cases:
#            mocker.get(
#                "http://cray-sls/v1/networks",
#                text=json.dumps(networks),
#                status_code=200
#            )
#            if expected_pool is None:
#                with self.assertRaises(werkzeug.exceptions.BadRequest):
#                    svc_type = self.uan_cfg_svc_customer_access.get_svc_type(
#                        service_type="ssh"
#                    )
#            else:
#                svc_type = self.uan_cfg_svc_customer_access.get_svc_type(
#                    service_type="ssh"
#                )
#                self.assertEqual(svc_type['ip_pool'], expected_pool)
#                self.assertEqual(svc_type['svc_type'], "LoadBalancer")
#                self.assertEqual(svc_type['subdomain'], expected_subdomain)
#        self.__reset_runtime_config()

    # pylint: disable=missing-docstring
    def test_get_service_type_bican_no_require(self, mocker): #pylint: disable=no-self-use
        if 'REQUIRE_BICAN' in os.environ:
            del os.environ['REQUIRE_BICAN']
#        self.__get_service_types_bican(mocker)

    # pylint: disable=missing-docstring
    def test_get_service_type_bican_require_false(self, mocker): #pylint: disable=no-self-use
        os.environ['REQUIRE_BICAN'] = "False" # use weird case to test lower
#        self.__get_service_types_bican(mocker)

    # pylint: disable=missing-docstring
    def test_get_service_type_bican_require_true(self, mocker): #pylint: disable=no-self-use
        os.environ['REQUIRE_BICAN'] = "True" # use weird case to test lower
#        self.__get_service_types_bican(mocker)


if __name__ == '__main__':
    unittest.main()

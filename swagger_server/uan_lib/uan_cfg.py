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
"""
   Manages Cray User Access Node instances.
"""

import json
import yaml
from flask import abort
#from kubernetes import client
import requests
from swagger_server.uan_lib.uan_logging import logger


#pylint: disable=too-few-public-methods
class UanCfg:
    """
    The UanCfg class provides the site configuration data to the
    User Access Node.
    """
    def __init__(self, uan_cfg='/etc/uan/cray-uan-mgr.yaml'):
        """Constructor

        """
        self.uan_cfg = uan_cfg

    def get_config(self):
        """Load the configuration from the configmap.

        This loads in the UAN Manager configmap to obtain the
        configuration settings for the UAN Manager.  For items that
        are managed under ETCD, the configmap is used the first time
        UAN Manager runs on a new system to load the initial settings
        into ETCD and then ignored from then on.  For items that are
        only configured in the configmap, updates to the configmap
        will be read in each time this is called.

        """
        cfg = {}
        try:
            with open(self.uan_cfg, encoding='utf-8') as uancfg:
                # pylint: disable=no-member
                cfg = yaml.load(uancfg, Loader=yaml.FullLoader)
        except (TypeError, IOError):
            abort(404, "configmap %s not found" % self.uan_cfg)
        # The empty case can be parsed as None, fix that...
        if cfg is None:
            cfg = {}

        return cfg


    @staticmethod
    def __get_sls_networks(): #pylint: disable=unused-private-member
        """Call into the SLS to get the list of configured networks

        """
        logger.debug("retrieving SLS network data")
        try:
            response = requests.get("http://cray-sls/v1/networks")
            # raise exception for 4XX and 5XX errors
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            logger.warning(
                "retrieving BICAN information %r %r", type(err), err
            )
            return []
        except Exception as err:  # pylint: disable=broad-except
            logger.warning(
                "retrieving BICAN information %r %r", type(err), err
            )
            return []
        try:
            ret = response.json() or []
        except json.decoder.JSONDecodeError as err:
            logger.warning(
                "decoding BICAN information %r %r", type(err), err
            )
            return []
        logger.debug("retrieved SLS network data: %s", ret)
        return ret

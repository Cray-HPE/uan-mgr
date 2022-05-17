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

import os
import json
import yaml
from flask import abort
from kubernetes import client
import requests
from swagger_server.uan_lib.uan_logging import logger


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
    def __get_sls_networks():
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

    @classmethod
    def __get_bican_pool(cls):
        """Learn the Bifurcated CAN address pool to be
        used (CHN or CAN) for user access.  If the pool can't be
        learned, then either use a default of 'customer_access' if
        REQUIRE_BICAN is false or not set, or fail with an informative
        error message.

        """
        # Declare a default BiCAN setting to use if none can be found.
        # Note that the SystemDefaultRoute (which would normally be
        # 'CAN' or 'CHN' is None here, that signals that no BiCAN
        # config was found in case we are enforcing BiCAN existence.
        default_props = {
            'SystemDefaultRoute': None
        }
        default_bican = {
            'Name': "BICAN",
            'ExtraProperties': default_props,
        }
        pool_map = {
            'CAN': "customer-access",
            'CHN': "customer-high-speed",
            'CMN': "customer-access",
        }
        logger.debug("getting require_bican")
        require_bican = os.environ.get('REQUIRE_BICAN', 'false').lower()
        logger.debug("require_bican = %s", require_bican)
        default_pool = (
            "customer-access" if require_bican == 'false'
            else None
        )
        logger.debug("default_pool = %s", default_pool)
        networks = cls.__get_sls_networks()
        bican_list = [net for net in networks if net['Name'] == "BICAN"]
        bican = bican_list[0] if bican_list else default_bican
        bican_props = bican.get('ExtraProperties', default_props)
        logger.debug("bican_props: %s", bican_props)
        pool = pool_map.get(bican_props['SystemDefaultRoute'], default_pool)
        logger.debug("pool = %s", pool)
        if pool is None:
            # Didn't find a pool and this system doesn't allow a
            # default pool so fail here.
            logger.error(
                "can't find valid BiCAN config in SLS: networks = %s",
                networks
            )
            msg = (
                "Bifurcated CAN configuration is required on the host system "
                "and could not be found.  If there is no Bifurcated "
                "CAN on this platform, ask your system administrator "
                "to set 'require_bican' to false in the site "
                "customizations for cray-uan-mgr."
            )
            abort(400, msg)
        return pool

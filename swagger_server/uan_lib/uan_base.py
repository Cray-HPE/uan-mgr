#
# MIT License
#
# (C) Copyright 2020, 2022 Hewlett Packard Enterprise Development LP
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
"""
Base Class for User Access Service Operations

Copyright 2020 Hewlett Packard Enterprise Development LP
"""

from kubernetes import config
from kubernetes.client import Configuration
from swagger_server.uan_lib.uan_cfg import UanCfg

#pylint: disable=too-few-public-methods
class UanBase:
    """Base class used for any class implementing UAN API functionality.
    Takes care of common activities like K8s client setup, loading UAN
    configuration from the default configmap and so forth.

    """
    def __init__(self):
        """ Constructor """
        config.load_incluster_config()
        try:
            k8s_config = Configuration().get_default_copy()
        except AttributeError:
            k8s_config = Configuration()
            k8s_config.assert_hostname = False
        Configuration.set_default(k8s_config)
        self.uas_cfg = UanCfg()

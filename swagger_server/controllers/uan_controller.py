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
"""UAN Server Controller

"""

import io

from swagger_server import version
from swagger_server.uan_lib.uan_mgr import UanManager
from swagger_server.uan_lib.uan_cfg import UanCfg


uan_cfg = UanCfg()  # pylint: disable=invalid-name


def get_uas_mgr_info():
    """List uas-mgr service info

    List uas-mgr service info

    :rtype: object
    """
    # This API call is used as a readiness check which provides a sort
    # of heartbeat for UAS, and we need a background activity to check
    # for stale UAIs and reap them.  The following provides the hook
    # for that and avoids the need for threading.  For now we will
    # reap the default number of UAIs at a go.  In the future this may
    # want to be configurable.
    UanManager().reap_uais()
    uan_mgr_info = {
        'service_name': 'cray-uan-mgr',
        'version': version
    }
    return uan_mgr_info

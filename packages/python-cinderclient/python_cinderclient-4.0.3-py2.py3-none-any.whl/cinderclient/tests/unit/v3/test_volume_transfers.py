# Copyright 2018 FiberHome Telecommunication Technologies CO.,LTD
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cinderclient import api_versions
from cinderclient.tests.unit import utils
from cinderclient.tests.unit.v3 import fakes


# Create calls need the right version of faked client
v3cs = fakes.FakeClient(api_versions.APIVersion('3.55'))
# Other calls fall back to default behavior
cs = fakes.FakeClient()


class VolumeTransfersTest(utils.TestCase):

    def test_create(self):
        vol = v3cs.transfers.create('1234')
        v3cs.assert_called('POST', '/volume-transfers',
                         body={'transfer': {'volume_id': '1234', 'name': None,
                                            'no_snapshots': False}})
        self._assert_request_id(vol)

    def test_create_without_snapshots(self):
        vol = v3cs.transfers.create('1234', no_snapshots=True)
        v3cs.assert_called('POST', '/volume-transfers',
                         body={'transfer': {'volume_id': '1234', 'name': None,
                                            'no_snapshots': True}})
        self._assert_request_id(vol)

    def test_get(self):
        transfer_id = '5678'
        vol = cs.transfers.get(transfer_id)
        cs.assert_called('GET', '/os-volume-transfer/%s' % transfer_id)
        self._assert_request_id(vol)

    def test_list(self):
        lst = cs.transfers.list()
        cs.assert_called('GET', '/os-volume-transfer/detail')
        self._assert_request_id(lst)

    def test_delete(self):
        b = cs.transfers.list()[0]
        vol = b.delete()
        cs.assert_called('DELETE', '/os-volume-transfer/5678')
        self._assert_request_id(vol)
        vol = cs.transfers.delete('5678')
        self._assert_request_id(vol)
        cs.assert_called('DELETE', '/os-volume-transfer/5678')
        vol = cs.transfers.delete(b)
        cs.assert_called('DELETE', '/os-volume-transfer/5678')
        self._assert_request_id(vol)

    def test_accept(self):
        transfer_id = '5678'
        auth_key = '12345'
        vol = cs.transfers.accept(transfer_id, auth_key)
        cs.assert_called('POST', '/os-volume-transfer/%s/accept' % transfer_id)
        self._assert_request_id(vol)

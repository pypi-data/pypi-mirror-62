# Copyright 2017-present Adtran, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from voltha_protos.events_pb2 import EventType, EventCategory, EventSubCategory
from pyvoltha.adapters.extensions.events.adapter_events import DeviceEventBase

class OnuTempRedEvent(DeviceEventBase):
    """
    The ONU Temperature Yellow Event is reported by both the CircuitPack
    (ME #6) and the ONT-G (ME # 256) to indicate no service has been shut
    down to avoid equipment damage. The operational state of the affected
    PPTPs indicates the affected services.

    For CircuitPack equipment events, the intf_id reported is that of the
    UNI's logical port number

    For ONT-G equipment events, the intf_id reported is that of the PON/ANI
    physical port number
    """
    def __init__(self, event_mgr, onu_id, intf_id, serial_number, raised_ts):
        super(OnuTempRedEvent, self).__init__(event_mgr, raised_ts, object_type='onu temperature red',
                                              event='ONU_TEMP_RED',
                                              category=EventCategory.ENVIRONMENT,
                                              sub_category=EventSubCategory.ONU)
        self._onu_id = onu_id
        self._intf_id = intf_id
        self._serial_number = serial_number

    def get_context_data(self):
        return {'onu-id': self._onu_id,
                'onu-intf-id': self._intf_id,
                'onu-serial-number': self._serial_number}

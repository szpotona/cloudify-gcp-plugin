# #######
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from gcp.gcp import GoogleCloudPlatform, GCPHttpError
from gcp.compute import constants


class Operation(GoogleCloudPlatform):
    def __init__(self, config, logger, name):
        super(Operation, self).__init__(config, logger, name)
        self.last_response = None

    def get_global_operation(self):
        return self.discovery.globalOperations().get(project=self.project,
                                                     operation=self.name)

    def get_zone_operation(self):
        return self.discovery.zoneOperations().get(project=self.project,
                                                   zone=self.zone,
                                                   operation=self.name)

    def is_success(self, refresh=False):
        self._update_if_necessary(refresh)
        return self.last_response['status'] == constants.OPERATION_DONE and \
            'error' not in self.last_response

    def is_error(self, refresh=False):
        self._update_if_necessary(refresh)
        return self.last_response['status'] == constants.OPERATION_DONE and \
            'error' in self.last_response

    def is_not_finished(self, refresh=False):
        self._update_if_necessary(refresh)
        return self.last_response['status'] != constants.OPERATION_DONE

    def refresh(self):
        self._update_if_necessary(True)

    def _get_operation(self):
        try:
            operation = self.get_global_operation()
        except GCPHttpError:
            operation = self.get_zone_operation()
        self.last_response = operation
        return self.last_response

    def _update_if_necessary(self, refresh):
        if refresh or self.last_status is None:
            self.get_operation()

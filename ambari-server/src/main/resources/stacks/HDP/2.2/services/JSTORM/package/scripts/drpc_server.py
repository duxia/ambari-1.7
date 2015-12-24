#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
from resource_management import *
from storm import storm
from service import service
from service_check import ServiceCheck


class DrpcServer(Script):
  def install(self, env):
    print 'install drpc ...'
    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)

    storm()

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)

    service("drpc", action="start")

  def stop(self, env):
    import params
    env.set_params(params)

    service("drpc", action="stop")

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.pid_drpc)

if __name__ == "__main__":
  DrpcServer().execute()
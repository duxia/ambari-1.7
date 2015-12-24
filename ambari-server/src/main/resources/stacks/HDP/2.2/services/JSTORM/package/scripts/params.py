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

from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import status_params

# server configurations
config = Script.get_config()

jstorm_user = config['configurations']['jstorm-env']['jstorm_user']
user_group = 'root'

log_dir = config['configurations']['jstorm-env']['jstorm_log_dir']
pid_dir = status_params.pid_dir

local_dir = config['configurations']['jstorm-site']['storm.local.dir|jstorm']
conf_dir = config['configurations']['jstorm-site']['_storm.conf.dir|jstorm']
tomcat_dir = config['configurations']['jstorm-site']['_storm.tomcat.dir|jstorm']
jstorm_bin_dir = local_dir+"/bin"

java64_home = config['hostLevelParams']['java_home']
jps_binary = format("{java64_home}/bin/jps")

storm_env_sh_template = config['configurations']['jstorm-env']['content']

if 'ganglia_server_host' in config['clusterHostInfo'] and \
    len(config['clusterHostInfo']['ganglia_server_host'])>0:
  ganglia_installed = True
  ganglia_server = config['clusterHostInfo']['ganglia_server_host'][0]
  ganglia_report_interval = 60
else:
  ganglia_installed = False

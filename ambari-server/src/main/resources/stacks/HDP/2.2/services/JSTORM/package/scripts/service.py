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


from resource_management import *
import time


def service(
    name,
    action='start'):
  import params
  import status_params

  pid_file = status_params.pid_files[name]
  no_op_test = format("ls {pid_file} >/dev/null 2>&1 && ps `cat {pid_file}` >/dev/null 2>&1")

  if name == "logviewer":
    tries_count = 12
  else:
    tries_count = 6

  if name == 'ui':
    process_grep = "apache.catalina.startup.Bootstrap$"
  else:
    process_grep = format("jstorm.*.{name}")
    
  find_proc = format("{jps_binary} -l  | grep {process_grep}")
  write_pid = format("{find_proc} | awk {{'print $1'}} > {pid_file}")
  crt_pid_cmd = format("{find_proc} && {write_pid}")

  if action == "start":
    if name == "ui":
      cmd = format("{tomcat_dir}/bin/startup.sh > {log_dir}/{name}.out 2>&1")

      Execute(cmd,
             not_if=no_op_test,
             user='root'
      )
      Execute(crt_pid_cmd,
              user=params.jstorm_user,
              logoutput=True,
              tries=tries_count,
              try_sleep=10,
              path=params.jstorm_bin_dir
      )
    else:
      cmd = format("env JAVA_HOME={java64_home} PATH=$PATH:{java64_home}/bin jstorm {name} > {log_dir}/{name}.out 2>&1")

      Execute(cmd,
             not_if=no_op_test,
             user=params.jstorm_user,
             wait_for_finish=False,
             path=params.jstorm_bin_dir
      )
      Execute(crt_pid_cmd,
              user=params.jstorm_user,
              logoutput=True,
              tries=tries_count,
              try_sleep=10,
              path=params.jstorm_bin_dir
      )

  elif action == "stop":
    if name == "ui":
      cmd = format("{tomcat_dir}/bin/shutdown.sh")
      Execute(cmd,
              user='root'
      )
      Execute(format("rm -f {pid_file}"))
    else:
      process_dont_exist = format("! ({no_op_test})")
      pid = format("`cat {pid_file}` >/dev/null 2>&1")
      Execute(format("kill {pid}"),
              not_if=process_dont_exist
      )
      Execute(format("kill -9 {pid}"),
              not_if=format("sleep 2; {process_dont_exist} || sleep 20; {process_dont_exist}"),
              ignore_failures=True
      )
      Execute(format("rm -f {pid_file}"))

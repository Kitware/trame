#!/usr/bin/env bash

deploy_uid=$(stat -c '%u' /deploy)
deploy_gid=$(stat -c '%g' /deploy)

trame_user_uid=$(id -u trame-user)
trame_user_gid=$(id -g trame-user)

run_chown=false
if [[ "$deploy_uid" != "$trame_user_uid" ]]; then
  usermod --uid $deploy_uid trame-user
  run_chown=true
fi

if [[ "$deploy_gid" != "$trame_user_gid" ]]; then
  groupmod --gid $deploy_gid trame-user
  run_chown=true
fi

if [[ "$run_chown" == false ]]; then
  exit 0
fi

# Run chown on all trame-user directories/files
chown -R trame-user:trame-user /opt/trame
chown trame-user:proxy-mapping /opt/trame/proxy-mapping.txt

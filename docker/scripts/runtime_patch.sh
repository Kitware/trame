#!/usr/bin/env bash

# Remap trame-user to a file/directory owner (TRAME_USER_DATA)
if [ -d "$TRAME_USER_DATA" ]
then
    new_uid=$(stat -c '%u' $TRAME_USER_DATA)
    new_gid=$(stat -c '%g' $TRAME_USER_DATA)
    trame_uid=$(id -u trame-user)
    trame_gid=$(id -g trame-user)
    if [[ "$new_uid" != "$trame_uid" ]]; then
        usermod --uid $new_uid trame-user
    fi
    if [[ "$new_gid" != "$trame_gid" ]]; then
        groupmod --gid $new_gid trame-user
    fi
fi

# Remap internal docker group to the group of /var/run/docker.sock
# This is to support docker-in-docker when /var/run/docker.sock is mounted
dnd_socket=/var/run/docker.sock
if [ -S $dnd_socket ]
then
    docker_gid=$(stat -c '%g' $dnd_socket)
    groupmod --gid $docker_gid docker
fi

#!/usr/bin/env bash

# Remap trame-user to a file/directory owner (TRAME_USER_DATA)
if [[ -n "$TRAME_USER_DATA" ]]
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
    
    # Run chown on all trame-user directories/files
    chown -R trame-user:trame-user /opt/trame
    chown trame-user:proxy-mapping /opt/trame/proxy-mapping.txt
    find /deploy -exec chown trame-user:trame-user {} \;
    chown -R trame-user:trame-user /deploy
fi

# Remap internal docker group to the group of /var/run/docker.sock
# This is to support docker-in-docker when /var/run/docker.sock is mounted
dnd_socket=/var/run/docker.sock
if [ -S $dnd_socket ]
then
    docker_gid=$(stat -c '%g' $dnd_socket)
    groupmod --gid $docker_gid docker
fi

# Patch Apache configuration to add prefix
if [[ -n "$TRAME_URL_PREFIX" ]]
then
    # Fix Apache
    TEMPLATE_INPUT=/opt/trame/apache.tpl
    CONFIG_OUTPUT=/etc/apache2/sites-available/001-trame.conf

    OUTPUT=$(<"${TEMPLATE_INPUT}")

    REPLACEMENT_STRING="TRAME_URL_PREFIX"
    OUTPUT="${OUTPUT//$REPLACEMENT_STRING/$TRAME_URL_PREFIX}"
    echo -e "$OUTPUT" > "${CONFIG_OUTPUT}"

    service apache2 restart

    # Fix index.html <base href=".">
    FILE_TO_PATCH=/deploy/server/www/index.html
    OUTPUT=$(<"${FILE_TO_PATCH}")
    BASE_OLD='<base href=".">'
    BASE_NEW="<base href=\"$TRAME_URL_PREFIX/\">"
    OUTPUT="${OUTPUT//$BASE_OLD/$BASE_NEW}"
    echo -e "$OUTPUT" > "${FILE_TO_PATCH}"
fi

podman run \
    --name mapml_panel_cont \
    -p 8090:8090 \
    -v <some local directory>/app:/home/app:Z \
    --net slirp4netns:allow_host_loopback=true \
    --detach rpcavaco/mapml_panel


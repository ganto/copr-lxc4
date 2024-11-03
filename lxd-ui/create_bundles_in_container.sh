#!/bin/bash -eu
#
# create vendor and webpack bundles inside a container (for reproducibility):
#
#   ./create_bundles_in_container.sh --security-opt label=disable

cat <<EOF | podman build -t lxd-ui-build -f - .
FROM fedora:39

RUN dnf upgrade -y && \
    dnf install -y rpmdevtools python3-packaging python3-pyyaml nodejs yarnpkg

WORKDIR /tmp/lxd-ui-build
COPY lxd-ui.spec create_bundles.sh

RUN mkdir bundles
CMD ./create_bundles.sh && mv *.tar.* bundles
EOF

podman run --name lxd-ui-build --replace "$@" lxd-ui-build
podman cp lxd-ui-build:bundles/. .

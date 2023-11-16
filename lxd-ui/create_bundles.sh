#!/bin/bash -eux
VERSION=$(rpm --specfile ./*.spec --qf '%{VERSION}\n' | head -1)
RELEASE=$(rpm --specfile ./*.spec --qf '%{RELEASE}\n' | head -1 | cut -d. -f2)
CHANGELOGTIME=$(rpm --specfile ./*.spec --qf '%{CHANGELOGTIME}\n' | head -1)
SOURCE_DATE_EPOCH=$((CHANGELOGTIME - CHANGELOGTIME % 86400))

SOURCE_DIR=lxd-ui-$VERSION
SOURCE_TAR=lxd-ui-$VERSION.tar.gz
VENDOR_TAR=lxd-ui-vendor-$VERSION-$RELEASE.tar.xz

## Download and extract source tarball
spectool -g lxd-ui.spec
rm -rf "${SOURCE_DIR}"
tar xf "${SOURCE_TAR}"

## Create vendor bundle
pushd "${SOURCE_DIR}"

# Vendor Node.js dependencies
export HUSKY=0
yarn install --frozen-lockfile
mv /usr/local/share/.cache .

popd

# Create tarball
# shellcheck disable=SC2046
XZ_OPT=-9 tar \
    --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH}" --clamp-mtime \
    --owner=0 --group=0 --numeric-owner \
    -cJf "${VENDOR_TAR}" \
    "${SOURCE_DIR}/.cache"

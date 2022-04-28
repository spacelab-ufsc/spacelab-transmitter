#! /bin/sh

SW_NAME=spacelab_transmitter
PKT_VERSION=0.1.0
DIST=ubuntu
DIST_VERSION=20.04
PYTHON_VERSION=3.9
PKT_NAME=${SW_NAME}_${PKT_VERSION}_${DIST}${DIST_VERSION}-1

SW_ICON=../${SW_NAME}/data/img/spacelab_transmitter_256x256.png

mkdir /tmp/${PKT_NAME}
mkdir /tmp/${PKT_NAME}/DEBIAN
mkdir /tmp/${PKT_NAME}/usr
mkdir /tmp/${PKT_NAME}/usr/bin
mkdir /tmp/${PKT_NAME}/usr/lib
mkdir /tmp/${PKT_NAME}/usr/lib/python${PYTHON_VERSION}
mkdir /tmp/${PKT_NAME}/usr/lib/python${PYTHON_VERSION}/site-packages
mkdir /tmp/${PKT_NAME}/usr/lib/python${PYTHON_VERSION}/site-packages/${SW_NAME}
mkdir /tmp/${PKT_NAME}/usr/local
mkdir /tmp/${PKT_NAME}/usr/local/bin
mkdir /tmp/${PKT_NAME}/usr/share
mkdir /tmp/${PKT_NAME}/usr/share/applications
mkdir /tmp/${PKT_NAME}/usr/share/icons
mkdir /tmp/${PKT_NAME}/usr/share/${SW_NAME}

cat > /tmp/${PKT_NAME}/DEBIAN/control << 'EOF'
Package: spacelab-transmitter
Version: 0.1-0
Section: hamradio
Priority: optional
Architecture: all
Depends: python3 (>= 3.6.5-3), python3-gi (>= 3.36.0-1)
Maintainer: Gabriel Mariano Marcelino <gabriel.mm8@gmail.com>
Description: SpaceLab packet transmitter.
EOF

tar -xf ../dist/${SW_NAME}-${PKT_VERSION}.tar.gz -C /tmp/

# bin
cat > /tmp/${PKT_NAME}/usr/bin/${SW_NAME} << 'EOF'
#!/usr/bin/python3
# EASY-INSTALL-ENTRY-SCRIPT: 'spacelab-transmitter==0.1.0','gui_scripts','spacelab-transmitter'
import re
import sys

# for compatibility with easy_install; see #2198
__requires__ = 'spacelab-transmitter==0.1.0'

try:
    from importlib.metadata import distribution
except ImportError:
    try:
        from importlib_metadata import distribution
    except ImportError:
        from pkg_resources import load_entry_point


def importlib_load_entry_point(spec, group, name):
    dist_name, _, _ = spec.partition('==')
    matches = (
        entry_point
        for entry_point in distribution(dist_name).entry_points
        if entry_point.group == group and entry_point.name == name
    )
    return next(matches).load()


globals().setdefault('load_entry_point', importlib_load_entry_point)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(load_entry_point('spacelab-transmitter==0.1.0', 'gui_scripts', 'spacelab-transmitter')())
EOF

# lib
cp -r /tmp/${SW_NAME}-${PKT_VERSION}/${SW_NAME}.egg-info /tmp/${PKT_NAME}/usr/lib/python${PYTHON_VERSION}/site-packages/
cp ../spacelab_transmitter/*.py /tmp/${PKT_NAME}/usr/lib/python${PYTHON_VERSION}/site-packages/${SW_NAME}/

# share
cp ../${SW_NAME}.desktop /tmp/${PKT_NAME}/usr/share/applications/
cp ${SW_ICON} /tmp/${PKT_NAME}/usr/share/icons/
cp ../${SW_NAME}/data/satellites/*.json /tmp/${PKT_NAME}/usr/share/${SW_NAME}/
cp ../${SW_NAME}/data/img/spacelab-logo-full-400x200.png /tmp/${PKT_NAME}/usr/share/${SW_NAME}/
cp ../${SW_NAME}/data/ui/${SW_NAME}.glade /tmp/${PKT_NAME}/usr/share/${SW_NAME}/

dpkg-deb --build /tmp/$PKT_NAME/

cp /tmp/${PKT_NAME}.deb .

rm -r /tmp/${SW_NAME}-${PKT_VERSION}
rm -r /tmp/${PKT_NAME}
rm /tmp/${PKT_NAME}.deb

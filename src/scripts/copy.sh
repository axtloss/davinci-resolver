#!/usr/bin/bash

INSTALLER_CACHE="${XDG_DATA_HOME}/installerCache"
INSTALLATION_DIRECTORY="${XDG_DATA_HOME}/installations/${1}"

mkdir -p "${INSTALLATION_DIRECTORY}"

pushd "${INSTALLER_CACHE}"

${INSTALLER_CACHE}/DaVinci_Resolve_*_Linux.run --appimage-extract

chmod -R u+rwX,go+rX,go-w "${INSTALLER_CACHE}/squashfs-root"

pushd "${INSTALLER_CACHE}/squashfs-root/share/panels"
tar -zxvf dvpanel-framework-linux-x86_64.tgz
chmod -R u+rwX,go+rX,go-w "${INSTALLER_CACHE}/squashfs-root/share/panels/lib"

mv *.so "${INSTALLER_CACHE}/squashfs-root/libs"
mv lib/* "${INSTALLER_CACHE}/squashfs-root/libs"
popd

mkdir -p -m 0755 "${INSTALLATION_DIRECTORY}/"{configs,DolbyVision,easyDCP,Fairlight,GPUCache,logs,Media,"Resolve Disk Database",.crashreport,.license,.LUT}

rm -rf "${INSTALLER_CACHE}"/squashfs-root/installer "${INSTALLER_CACHE}"/squashfs-root/installer* "${INSTALLER_CACHE}"/squashfs-root/AppRun "${INSTALLER_CACHE}"/squashfs-root/AppRun*

cp -rf "${INSTALLER_CACHE}"/squashfs-root/* "${INSTALLATION_DIRECTORY}"

pushd "${INSTALLATION_DIRECTORY}"

install -Dm0644 share/default-config.dat -t "${INSTALLATION_DIRECTORY}/configs"
install -Dm0644 share/log-conf.xml -t "${INSTALLATION_DIRECTORY}/configs"
install -Dm0644 share/default_cm_config.bin -t "${INSTALLATION_DIRECTORY}/DolbyVision"

install -Dm0644 graphics/DV_Resolve.png -t "${pkgdir}/usr/share/icons/hicolor/64x64/apps"
install -Dm0644 graphics/DV_ResolveProj.png -t "${pkgdir}/usr/share/icons/hicolor/64x64/apps"
install -Dm0644 share/resolve.xml -t "${pkgdir}/usr/share/mime/packages"
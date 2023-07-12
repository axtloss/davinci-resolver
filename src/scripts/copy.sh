#!/usr/bin/bash

INSTALLER_CACHE="${XDG_DATA_HOME}/installerCache"
INSTALLATION_DIRECTORY="${XDG_DATA_HOME}/installations/${1}"

mkdir -p "${INSTALLATION_DIRECTORY}"

pushd "${INSTALLER_CACHE}"

chmod +x ${INSTALLER_CACHE}/DaVinci_Resolve_*_Linux.run
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

install -Dm0644 graphics/DV_Resolve.png -t "${INSTALLATION_DIRECTORY}/usr/share/icons/hicolor/64x64/apps"
install -Dm0644 graphics/DV_ResolveProj.png -t "${INSTALLATION_DIRECTORY}/usr/share/icons/hicolor/64x64/apps"
install -Dm0644 share/resolve.xml -t "${INSTALLATION_DIRECTORY}/usr/share/mime/packages"

while IFS= read -r -d '' i; do
		[[ -f "${i}" && $(od -t x1 -N 4 "${i}") == *"7f 45 4c 46"* ]] || continue
		patchelf --set-rpath \
"${INSTALLATION_DIRECTORY}'/libs:'\
"${INSTALLATION_DIRECTORY}'/libs/plugins/sqldrivers:'\
"${INSTALLATION_DIRECTORY}'/libs/plugins/xcbglintegrations:'\
"${INSTALLATION_DIRECTORY}'/libs/plugins/imageformats:'\
"${INSTALLATION_DIRECTORY}'/libs/plugins/platforms:'\
"${INSTALLATION_DIRECTORY}'/libs/Fusion:'\
"${INSTALLATION_DIRECTORY}'/plugins:'\
"${INSTALLATION_DIRECTORY}'/bin:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/BlackmagicRawAPI:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/plugins/platforms:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/plugins/imageformats:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/plugins/mediaservice:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/plugins/audio:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/plugins/xcbglintegrations:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWSpeedTest/plugins/bearer:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/BlackmagicRawAPI:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/plugins/mediaservice:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/plugins/imageformats:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/plugins/audio:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/plugins/platforms:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/plugins/xcbglintegrations:'\
"${INSTALLATION_DIRECTORY}'/BlackmagicRAWPlayer/plugins/bearer:'\
"${INSTALLATION_DIRECTORY}'/Onboarding/plugins/xcbglintegrations:'\
"${INSTALLATION_DIRECTORY}'/Onboarding/plugins/qtwebengine:'\
"${INSTALLATION_DIRECTORY}'/Onboarding/plugins/platforms:'\
"${INSTALLATION_DIRECTORY}'/Onboarding/plugins/imageformats:'\
"${INSTALLATION_DIRECTORY}'/DaVinci Control Panels Setup/plugins/platforms:'\
"${INSTALLATION_DIRECTORY}'/DaVinci Control Panels Setup/plugins/imageformats:'\
"${INSTALLATION_DIRECTORY}'/DaVinci Control Panels Setup/plugins/bearer:'\
"${INSTALLATION_DIRECTORY}'/DaVinci Control Panels Setup/AdminUtility/PlugIns/DaVinciKeyboards:'\
"${INSTALLATION_DIRECTORY}'/DaVinci Control Panels Setup/AdminUtility/PlugIns/DaVinciPanels:'\
'$ORIGIN' "${i}"
	done < <(find "${INSTALLATION_DIRECTORY}/" -type f -size -32M -print0)
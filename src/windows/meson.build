pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
windowsdir = join_paths(pkgdatadir, 'davinci_resolver/windows')

window_sources = [
  '__init__.py',
  'davinciInstallerWindow.py',
  'davinciInstallationView.py'
]

install_data(window_sources, install_dir: windowsdir)

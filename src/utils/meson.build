pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
utilsdir = join_paths(pkgdatadir, 'davinci_resolver/utils')

utils_sources = [
  '__init__.py',
  'davinciInstaller.py',
  'runAsync.py',
  'zipFile.py'
]

install_data(utils_sources, install_dir: utilsdir)

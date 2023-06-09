pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
classesdir = join_paths(pkgdatadir, 'davinci_resolver/classes')

classes_sources = [
  '__init__.py',
  'userData.py',
]

install_data(classes_sources, install_dir: classesdir)

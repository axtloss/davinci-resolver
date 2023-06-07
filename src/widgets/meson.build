pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
widgetsdir = join_paths(pkgdatadir, 'davinci_resolver/widgets')

widget_sources = [
  '__init__.py',
  'entry.py',
  'tag.py',
]

install_data(widget_sources, install_dir: widgetsdir)

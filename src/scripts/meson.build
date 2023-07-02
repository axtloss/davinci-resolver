pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
scriptsdir = join_paths(pkgdatadir, 'davinci_resolver/scripts')

scripts_sources = [
  'copy.sh',
]

install_data(scripts_sources, install_dir: scriptsdir)

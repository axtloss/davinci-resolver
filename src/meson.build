pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'davinci_resolver')
gnome = import('gnome')

gnome.compile_resources('davinci-resolver',
  'davinci-resolver.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'davinci-resolver.in',
  output: 'davinci-resolver',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

davinci_resolver_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  '../versions.json'
]

install_data(davinci_resolver_sources, install_dir: moduledir)

subdir('widgets')
subdir('classes')
subdir('utils')
subdir('windows')

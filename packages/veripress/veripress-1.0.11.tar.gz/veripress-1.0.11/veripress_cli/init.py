import os
import shutil
from datetime import datetime

import click

from veripress_cli import cli


@cli.command('init', short_help='Initialize a new instance directory.',
             help='This command will initialize the current working directory '
                  'as a new VeriPress instance, which means to create '
                  'default configuration file, necessary subdirectories, etc.')
@click.option('--storage-mode', '-s', default='file',
              type=click.Choice(['file']),
              help='Storage mode (only "file" mode supported currently).')
def init_command(storage_mode):
    from veripress import app
    instance_path = app.instance_path
    defaults_dir = os.path.join(os.path.dirname(__file__), 'defaults')

    with open(os.path.join(defaults_dir, 'config.py'),
              'r', encoding='utf-8') as f_default_conf:
        with open(os.path.join(instance_path, 'config.py'),
                  'w', encoding='utf-8') as f_conf:
            f_conf.write(
                f_default_conf.read().format(storage_mode=storage_mode))

    shutil.copyfile(os.path.join(defaults_dir, 'site.json'),
                    os.path.join(instance_path, 'site.json'))
    shutil.copytree(os.path.join(defaults_dir, 'static'),
                    os.path.join(instance_path, 'static'))
    os.mkdir(os.path.join(instance_path, 'themes'))

    if storage_mode == 'file':
        init_file_storage(instance_path)

    click.echo('\nDefault files and configurations has been created!\n\n'
               'Now you can run "veripress theme install default" to '
               'install the default theme and then run "veripress preview" '
               'to preview the blog.\n\nEnjoy!')


def init_file_storage(instance_path):
    os.mkdir(os.path.join(instance_path, 'posts'))
    os.mkdir(os.path.join(instance_path, 'pages'))
    os.mkdir(os.path.join(instance_path, 'widgets'))

    now_dt = datetime.now()
    first_post_file_path = os.path.join(
        instance_path, 'posts',
        '{}-hello-world.md'.format(now_dt.strftime('%Y-%m-%d'))
    )
    with open(first_post_file_path, 'w', encoding='utf-8') as f:
        f.write('---\n'
                'title: Hello, world!\n'
                'created: {}\n'
                'categories: Hello\n'
                'tags: [Hello, Greeting]\n'
                '---\n\n'.format(now_dt.strftime('%Y-%m-%d %H:%M:%S')))
        f.write('This is the hello world post!\n')

    os.mkdir(os.path.join(instance_path, 'pages', 'hello'))
    first_page_file_path = os.path.join(instance_path,
                                        'pages', 'hello', 'index.md')
    with open(first_page_file_path, 'w', encoding='utf-8') as f:
        f.write('---\n'
                'title: Hello\n'
                'created: {}\n'
                '---\n\n'.format(now_dt.strftime('%Y-%m-%d %H:%M:%S')))
        f.write('This is the hello custom page!\n')

    first_widget_file_path = os.path.join(instance_path,
                                          'widgets', 'welcome.md')
    with open(first_widget_file_path, 'w', encoding='utf-8') as f:
        f.write('---\n'
                'position: sidebar\n'
                'order: 0\n'
                '---\n\n')
        f.write('#### Welcome!\n\n'
                'Hi! Welcome to my blog.\n')

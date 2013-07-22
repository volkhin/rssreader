#-*- coding: utf-8 -*-
import time

from fabric.api import local, run, settings, env


project = 'rssreader'

def reset():
    '''
    Reset local env.
    '''
    local('python manage.py initdb')

def create_venv():
    local('virtualenv env')

def activate_venv():
    activate_this = 'env/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))


client_id = 'K6ZqPfgPPPihzZtdfMyrU'
api_key = '8lVFnTgT2Hgcwj09YZuiXTsduHhbPnDjlOQLqUXhn'


class DigitalOceanWrapper(object):
    REBUILD_EXISTING = False

    def __init__(self, client_id, api_key, name):
        from dop.client import Client
        self.name = name
        self.client = Client(client_id, api_key)

    def get_or_create_droplet(self, name):
        '''
        Find droplet by name or create new one.
        '''
        droplet = self.find_droplet(name)
        if droplet is not None and self.REBUILD_EXISTING:
            self.client.rebuild_droplet(droplet.id, droplet.image_id)
        if droplet is None:
            droplet = self.create_droplet(name)
        droplet_id = droplet.id
        while droplet.status in ['', 'new',]:
            print 'waiting...', droplet.to_json()
            time.sleep(5)
            droplet = self.client.show_droplet(droplet_id)
        return droplet

    def find_droplet(self, name):
        '''
        Find existing droplet by name.
        '''
        for droplet in self.client.show_active_droplets():
            if droplet.name == name:
                return droplet

    def create_droplet(self, name):
        '''
        Create new droplet with minimal disk and memory.
        '''
        print 'Creating new droplet...'
        size_id = [size.id for size in self.client.sizes()
                if size.name == u'512MB'][0]
        image_id = [image.id for image in self.client.images()
                if image.name == u'Ubuntu 12.04 x64'][0]
        region_id = [region.id for region in self.client.regions() if
                region.name == u'San Francisco 1'][0]
        ssh_keys = [str(key.id) for key in self.client.all_ssh_keys()]
        print size_id, image_id, region_id, ssh_keys
        droplet = self.client.create_droplet(name, size_id=size_id,
                image_id=image_id, region_id=region_id, ssh_key_ids=ssh_keys)
        return droplet

    def setup(self):
        '''
        Prepare droplet for deployment.
        '''
        import fabtools
        from fabtools import require
        droplet = self.get_or_create_droplet(self.name)
        print droplet.to_json()
        ip_address = droplet.ip_address
        with settings(host_string='root@{}'.format(ip_address)):
            run('uname -a')
            require.user('volkhin')
            require.sudoer('volkhin')


def digitalocean_deploy():
    '''
    Deploy on DigitalOcean.
    Create instance, install nginx & postgres & ...
    '''
    activate_venv()
    digital_ocean = DigitalOceanWrapper(client_id, api_key, 'rssreader')
    digital_ocean.setup()

def setup():
    '''
    Setup virtual env.
    '''
    create_venv()
    activate_venv()
    local('python setup.py develop')
    reset()

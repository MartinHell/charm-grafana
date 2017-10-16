from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class GrafanaProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:grafana-source}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:grafana-source}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')

    def provide(self, source_type, port, description, username=None, password=None):
        relation_info = {
            'type': source_type,
            'url': 'http://{}:{}'.format(hookenv.unit_get('private-address'), port),
            'description': description,
        }
        if username and password:
            relation_info['username'] = username
            relation_info['password'] = password

        self.set_remote(**relation_info)

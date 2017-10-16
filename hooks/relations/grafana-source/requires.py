from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class GrafanaRequires(RelationBase):
    scope = scopes.SERVICE

    @hook('{requires:grafana-source}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('type'):
            conv.set_state('{relation_name}.available')

    @hook('{requires:grafana-source}-relation-departed')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    def datasources(self):
        """
        Returns a list of available datasources

        The return value is a list of dicts of the following form::

            [
                {
                    'service_name': remote_service_name,
                    'type': endpoint_type, #  ie. prometheus
                    'url': endpoint_url,
                    'description': endpoint description,
                    'username': optional_username,
                    'password': optional_password,
                },
                # ...
            ]
        """
        datasources = []
        for conv in self.conversations():
            ds = {'service_name': conv.scope.split('/')[0],
                  'type': conv.get_remote('type'),
                  'url': conv.get_remote('url'),
                  'description': conv.get_remote('description')
                  }
            if conv.get_remote('username') and conv.get_remote('password'):
                ds['username'] = conv.get_remote('username')
                ds['password'] = conv.get_remote('password')
            datasources.append(ds)

        return datasources

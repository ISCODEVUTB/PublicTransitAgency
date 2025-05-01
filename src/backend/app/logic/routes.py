class Routes:
    def __init__(self, route: dict, route_id: str = None):
        self._route = route
        self._route_id = route_id if route_id is not None else route.get('route_id')

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, value: dict):
        self._route = value 
        if 'route_id' in value:
            self._route_id = value['route_id']

    @property
    def route_id(self):
        return self._route_id

    @route_id.setter
    def route_id(self, value: str):
        self._route_id = value
        self._route['route_id'] = value
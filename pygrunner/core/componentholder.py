from pygrunner.core.components import component_names

empty = object()

class ComponentHolder(object):
    """
    This allows to register and update components
    """

    def __init__(self):
        self.components = []
        for component_name in component_names:
            component = getattr(self, component_name, empty)
            if component is empty:
                setattr(self, component_name, None)
            else:
                component.register(self)

    def add_component(self, component):
        if getattr(self, component.name, None) is None:
            setattr(self, component.name, component)
            component.register(self)
            self.components.append(component)
        else:
            raise Exception("Can't register twice!")

    def add_components(self, components):
        for component in components:
            self.add_component(component)


    def update(self, dt):
        for component in self.components:
            component.update()

    def replace_component(self, component):
        current = getattr(self, component.name, None)
        if current is not None:
            self.remove_component(current)

        setattr(self, component.name, component)
        component.register(self)
        self.components.append(component)

    def remove_component(self, component):
        setattr(self, component.name, None)
        self.components.remove(component)
        component.reset()

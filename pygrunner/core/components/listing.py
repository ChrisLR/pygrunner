component_listing = []
component_names = set()

def register(component):
    component_listing.append(component)
    component_names.add(component.name)
    return component

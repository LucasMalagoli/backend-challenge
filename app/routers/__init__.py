import pkgutil
import importlib
import inspect
from fastapi import APIRouter


def get_routers(package_name="app.routers"):
    """
    Gets any router variables inside the `package_name` that are literally called "router"
    to make the process of registering new CRUD routers automatic.
    """
    routers = []

    # Discover all modules in app/routers by default
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        # Look for a variable named 'router' that is an APIRouter
        for name, obj in inspect.getmembers(module):
            if name == "router" and isinstance(obj, APIRouter):
                routers.append(obj)

    return routers

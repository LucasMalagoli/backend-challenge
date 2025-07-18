
import pkgutil
import importlib
import os

# Automatically import all model modules to avoid having dependecy issues
package_dir = os.path.dirname(__file__)
for (_, module_name, _) in pkgutil.iter_modules([package_dir]):
    importlib.import_module(f"{__name__}.{module_name}")

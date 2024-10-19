from .setup_project import TOYSHOWTOOLS_OT_setup_project
from .delete_lighting_setup import TOYSHOWTOOLS_OT_delete_lighting_setup
from .render_test import TOYSHOWTOOLS_OT_render_test

import bpy

classes = (
    TOYSHOWTOOLS_OT_setup_project,
    TOYSHOWTOOLS_OT_delete_lighting_setup,
    TOYSHOWTOOLS_OT_render_test,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
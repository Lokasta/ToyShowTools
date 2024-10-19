import bpy
import os
import json
import urllib.request
import ssl
import threading
from . import operators
from .properties import TOYSHOWTOOLS_Properties
from .operators.update import TOYSHOWTOOLS_OT_check_for_update, TOYSHOWTOOLS_OT_update_addon, check_for_update

bl_info = {
    "name": "Project Setup Helper",
    "author": "Your Name <your.email@example.com>",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Project Setup",
    "description": "Helper addon to set up project settings and manage lighting",
    "category": "Scene",
    "warning": "",  # Used to display update notifications
    "doc_url": "https://github.com/Lokasta/ToyShowTools",  # Documentation URL
}

class TOYSHOWTOOLS_PT_main_panel(bpy.types.Panel):
    bl_label = "Toy Show Tools"
    bl_idname = "TOYSHOWTOOLS_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ToyShowTools"

    def draw(self, context):
        layout = self.layout
        props = context.scene.toyshowtools_props

        layout.operator("toyshowtools.setup_project", text="Setup Project")
        layout.operator("toyshowtools.delete_lighting_setup", text="Delete Lighting Setup")
        
        # Separator
        layout.separator()

        # Frame Render Cadency Input
        layout.prop(props, "frame_cadency")

        # Render Test Button
        layout.operator("toyshowtools.render_test", text="Render Test")

class TOYSHOWTOOLS_PT_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        # Addon information
        col.label(text="Name: Project Setup Helper")
        col.label(text="Author: Your Name <your.email@example.com>")
        col.label(text="Version: 1.0.0")
        col.label(text="Blender: 4.2.0")
        col.label(text="Description: Helper addon to set up project settings and manage lighting")
        col.label(text="Documentation: https://github.com/Lokasta/ToyShowTools")

        # Separator
        col.separator()

        # Update functionality
        col.operator("toyshowtools.check_for_update", text="Check for Update")
        col.operator("toyshowtools.update_addon", text="Update Addon")

def register():
    bpy.utils.register_class(TOYSHOWTOOLS_Properties)
    bpy.types.Scene.toyshowtools_props = bpy.props.PointerProperty(type=TOYSHOWTOOLS_Properties)

    operators.register()
    bpy.utils.register_class(TOYSHOWTOOLS_PT_main_panel)
    bpy.utils.register_class(TOYSHOWTOOLS_PT_preferences)
    bpy.utils.register_class(TOYSHOWTOOLS_OT_check_for_update)
    bpy.utils.register_class(TOYSHOWTOOLS_OT_update_addon)

    # Check for updates on load
    threading.Thread(target=check_for_update).start()

def unregister():
    bpy.utils.unregister_class(TOYSHOWTOOLS_Properties)
    del bpy.types.Scene.toyshowtools_props

    operators.unregister()
    bpy.utils.unregister_class(TOYSHOWTOOLS_PT_main_panel)
    bpy.utils.unregister_class(TOYSHOWTOOLS_PT_preferences)
    bpy.utils.unregister_class(TOYSHOWTOOLS_OT_check_for_update)
    bpy.utils.unregister_class(TOYSHOWTOOLS_OT_update_addon)

if __name__ == "__main__":
    register()
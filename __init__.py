import bpy
from . import operators
from .properties import TOYSHOWTOOLS_Properties

bl_info = {
    "name": "ToyShowTools",
    "author": "Leon Maciel",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > ToyShowTools",
    "description": "Tools for Toy Show Project",
    "category": "Object",
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

def register():
    bpy.utils.register_class(TOYSHOWTOOLS_Properties)
    bpy.types.Scene.toyshowtools_props = bpy.props.PointerProperty(type=TOYSHOWTOOLS_Properties)

    operators.register()
    bpy.utils.register_class(TOYSHOWTOOLS_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(TOYSHOWTOOLS_PT_main_panel)
    operators.unregister()

    del bpy.types.Scene.toyshowtools_props
    bpy.utils.unregister_class(TOYSHOWTOOLS_Properties)

if __name__ == "__main__":
    register()
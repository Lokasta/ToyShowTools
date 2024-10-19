import bpy

class TOYSHOWTOOLS_Properties(bpy.types.PropertyGroup):
    frame_cadency: bpy.props.IntProperty(
        name="Frame Render Cadency",
        description="Interval between frames to render",
        default=10,
        min=5
    )
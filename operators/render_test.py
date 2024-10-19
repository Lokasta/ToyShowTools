import bpy
import os

class TOYSHOWTOOLS_OT_render_test(bpy.types.Operator):
    bl_label = "Render Test"
    bl_idname = "toyshowtools.render_test"
    bl_description = "Render frames at specified intervals and save to RenderTestFrames folder"

    def execute(self, context):
        scene = context.scene
        props = scene.toyshowtools_props

        # Ensure the frame cadency is at least 1
        cadency = max(1, props.frame_cadency)

        # Check if the Blender file is saved
        blend_dir = os.path.dirname(bpy.data.filepath)
        if not blend_dir:
            self.report({'ERROR'}, "Please save the Blender file before rendering.")
            return {'CANCELLED'}

        # Create RenderTestFrames directory
        render_dir = os.path.join(blend_dir, "RenderTestFrames")
        if not os.path.exists(render_dir):
            os.makedirs(render_dir)

        # Store original settings to restore later
        original_filepath = scene.render.filepath
        original_frame_step = scene.frame_step
        original_use_lock_interface = scene.render.use_lock_interface  # Changed here

        # Set up rendering settings
        scene.render.filepath = os.path.join(render_dir, "frame_")
        scene.frame_step = cadency
        scene.render.use_lock_interface = False  # Changed here

        # Render animation with frame step
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)

        # Restore original settings after rendering completes
        def restore_settings(scene):
            scene.render.filepath = original_filepath
            scene.frame_step = original_frame_step
            scene.render.use_lock_interface = original_use_lock_interface  # Changed here
            self.report({'INFO'}, "Render Test completed.")

            # Remove the handler after execution
            bpy.app.handlers.render_complete.remove(restore_settings)

        # Add a handler to restore settings after rendering completes
        bpy.app.handlers.render_complete.append(restore_settings)

        return {'FINISHED'}
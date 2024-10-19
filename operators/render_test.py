import bpy
import os

class TOYSHOWTOOLS_OT_render_test(bpy.types.Operator):
    bl_label = "Render Test Frames"
    bl_idname = "toyshowtools.render_test"
    bl_description = "Render frames at specified intervals and save to RenderTestFrames folder"

    def execute(self, context):
        scene = context.scene
        props = scene.toyshowtools_props

        # Ensure the frame cadency is at least 1
        cadency = max(1, props.frame_cadency)

        # Check if the Blender file is saved
        blend_filepath = bpy.data.filepath
        if not blend_filepath:
            self.report({'ERROR'}, "Please save the Blender file before rendering.")
            return {'CANCELLED'}

        blend_dir = os.path.dirname(blend_filepath)
        blend_filename = os.path.splitext(os.path.basename(blend_filepath))[0]

        # Remove spaces from the filename
        blend_filename = blend_filename.replace(" ", "")

        # Create _RenderTestFrames directory
        render_test_dir = os.path.join(blend_dir, "_RenderTestFrames")
        if not os.path.exists(render_test_dir):
            os.makedirs(render_test_dir)

        # Create subfolder inside _RenderTestFrames
        render_dir = os.path.join(render_test_dir, f"{blend_filename}_testframes")
        if not os.path.exists(render_dir):
            os.makedirs(render_dir)

        # Store original settings to restore later
        original_filepath = scene.render.filepath
        original_frame_step = scene.frame_step
        original_use_lock_interface = scene.render.use_lock_interface
        original_resolution_x = scene.render.resolution_x
        original_resolution_y = scene.render.resolution_y

        # Set up rendering settings
        scene.render.filepath = os.path.join(render_dir, "frame_")
        scene.frame_step = cadency
        scene.render.use_lock_interface = False
        scene.render.resolution_x = original_resolution_x // 2
        scene.render.resolution_y = original_resolution_y // 2

        # Render animation with frame step
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)

        # Restore original settings after rendering completes
        #scene.render.filepath = original_filepath
        scene.frame_step = original_frame_step
        scene.render.use_lock_interface = original_use_lock_interface
        scene.render.resolution_x = original_resolution_x
        scene.render.resolution_y = original_resolution_y

        self.report({'INFO'}, "Test rendering completed successfully.")
        return {'FINISHED'}
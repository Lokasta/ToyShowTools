import bpy
import os
import gpu

class TOYSHOWTOOLS_OT_setup_project(bpy.types.Operator):
    bl_label = "Setup Project"
    bl_idname = "toyshowtools.setup_project"
    bl_description = "Setup the project with specific settings"

    def execute(self, context):
        scene = context.scene

        # Set framerate to custom and set to 12 fps
        scene.render.fps = 12
        scene.render.fps_base = 1.0  # Ensure that fps_base is set to 1.0

        # Set resolution to 1920 x 1920
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1920

        # Set Render Engine to Cycles
        scene.render.engine = 'CYCLES'

        # Check GPU backend and device type
        backend_type = gpu.platform.backend_type_get()
        device_type = gpu.platform.device_type_get()

        # Enable GPU Rendering if a compatible GPU is found
        if backend_type in {'METAL', 'CUDA', 'OPTIX', 'HIP','OPENGL','VULKAN'} and device_type != 'SOFTWARE':
            scene.cycles.device = 'GPU'
        else:
            scene.cycles.device = 'GPU'
            self.report({'WARNING'}, "No compatible GPU found, using CPU for rendering.")

        # Set Viewport Sampling Settings
        scene.cycles.preview_samples = 100
        scene.cycles.preview_denoising = True

        # Set Render Sampling Settings
        scene.cycles.samples = 120
        scene.cycles.time_limit = 120  # Time limit in seconds
        scene.cycles.use_denoising = True

        # Set file format to PNG, RGBA color depth 16
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.image_settings.color_depth = '16'

        # Set output path to RENDER/filename/frame_
        blend_filepath = bpy.data.filepath
        if not blend_filepath:
            self.report({'ERROR'}, "Please save the Blender file before running this operator.")
            return {'CANCELLED'}

        blend_dir = os.path.dirname(blend_filepath)
        blend_filename = os.path.splitext(os.path.basename(blend_filepath))[0]

        # Remove spaces from the filename
        blend_filename = blend_filename.replace(" ", "")

        render_dir = os.path.join(blend_dir, 'RENDER', blend_filename)

        if not os.path.exists(render_dir):
            os.makedirs(render_dir)

        scene.render.filepath = os.path.join(render_dir, 'frame_')

        # Get all cameras in the scene
        cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']

        if not cameras:
            self.report({'WARNING'}, "No cameras found in the scene.")
            return {'CANCELLED'}

        # Load the background image
        addon_dir = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(addon_dir, "Resources", "frame_guide_square.png")

        if os.path.exists(image_path):
            try:
                image = bpy.data.images.load(image_path, check_existing=True)
            except RuntimeError as e:
                self.report({'ERROR'}, f"Failed to load image: {e}")
                return {'CANCELLED'}
        else:
            self.report({'ERROR'}, "Background image not found at: " + image_path)
            return {'CANCELLED'}

        # Add background image to all cameras
        for camera in cameras:
            cam_data = camera.data

            # Enable background images if not already
            if not cam_data.show_background_images:
                cam_data.show_background_images = True

            # Check if the image is already in background images
            bg_images = cam_data.background_images
            bg_image = None
            for bg in bg_images:
                if bg.image == image:
                    bg_image = bg
                    break

            if not bg_image:
                # Add new background image
                bg_image = bg_images.new()
                bg_image.image = image
                bg_image.display_depth = 'FRONT'  # Or 'BACK', depending on preference
                bg_image.alpha = 1.0  # Set transparency if needed
            else:
                # Update existing background image settings if needed
                bg_image.display_depth = 'FRONT'
                bg_image.alpha = 1.0

        self.report({'INFO'}, "Project setup completed successfully.")
        return {'FINISHED'}
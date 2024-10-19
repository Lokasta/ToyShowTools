import bpy

class TOYSHOWTOOLS_OT_delete_lighting_setup(bpy.types.Operator):
    bl_label = "Delete Lighting Setup"
    bl_idname = "toyshowtools.delete_lighting_setup"
    bl_description = "Delete all lights in the scene"

    def execute(self, context):
        lights = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
        for light in lights:
            bpy.data.objects.remove(light, do_unlink=True)
        self.report({'INFO'}, f"Deleted {len(lights)} light(s)")
        return {'FINISHED'}
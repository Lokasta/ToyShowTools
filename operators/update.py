import bpy
import urllib.request
import json
import threading
import ssl
import os

class TOYSHOWTOOLS_OT_check_for_update(bpy.types.Operator):
    bl_idname = "toyshowtools.check_for_update"
    bl_label = "Check for Updates"
    bl_description = "Check if a new version of the addon is available"

    def execute(self, context):
        threading.Thread(target=self.check_for_updates, args=(context,)).start()
        return {'FINISHED'}

    def check_for_updates(self, context):
        try:
            # Indicate that an update check is in progress
            context.window_manager.toyshowtools_updating = True

            # URL to the version.json file on GitHub
            version_url = "https://raw.githubusercontent.com/Lokasta/ToyShowTools/main/version.json"

            # Fetch the latest version.json from GitHub
            with urllib.request.urlopen(version_url, context=ssl._create_unverified_context()) as response:
                data = json.loads(response.read().decode())
                latest_version = tuple(data['version'])

            # Get current version
            current_version = bpy.context.preferences.addons[__name__].bl_info['version']

            # Compare versions
            if latest_version > current_version:
                context.window_manager.toyshowtools_update_available = True
                self.report({'INFO'}, f"Update available: {latest_version}")
            else:
                context.window_manager.toyshowtools_update_available = False
                self.report({'INFO'}, "You have the latest version.")

        except Exception as e:
            self.report({'ERROR'}, f"Failed to check for updates: {e}")
        finally:
            context.window_manager.toyshowtools_updating = False


class TOYSHOWTOOLS_OT_update_addon(bpy.types.Operator):
    bl_idname = "toyshowtools.update_addon"
    bl_label = "Update Addon"
    bl_description = "Download and install the latest version of the addon"

    def execute(self, context):
        threading.Thread(target=self.update_addon, args=(context,)).start()
        return {'FINISHED'}

    def update_addon(self, context):
        try:
            # Indicate that an update is in progress
            context.window_manager.toyshowtools_updating = True

            # Check if update is available
            if not context.window_manager.get('toyshowtools_update_available', False):
                self.report({'ERROR'}, "No update available. Please check for updates first.")
                return

            # Download the latest version
            latest_version_url = "https://github.com/Lokasta/ToyShowTools/archive/refs/heads/main.zip"
            self.report({'INFO'}, "Downloading the latest version...")
            zip_path = os.path.join(bpy.app.tempdir, "ToyShowTools_latest.zip")
            with urllib.request.urlopen(latest_version_url, context=ssl._create_unverified_context()) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())

            # Install the addon
            self.report({'INFO'}, "Installing the latest version...")
            bpy.ops.preferences.addon_install(filepath=zip_path, overwrite=True)
            bpy.ops.preferences.addon_enable(module='ToyShowTools')

            # Remove the temporary zip file
            os.remove(zip_path)

            self.report({'INFO'}, "Addon updated successfully. Please restart Blender.")

        except Exception as e:
            self.report({'ERROR'}, f"Failed to update addon: {e}")
        finally:
            context.window_manager.toyshowtools_updating = False
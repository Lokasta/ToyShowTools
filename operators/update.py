import bpy
import os
import json
import urllib.request
import ssl
import threading
import tempfile

GITHUB_REPO_URL = "https://api.github.com/repos/Lokasta/ToyShowTools/releases/latest"
ADDON_DIR = os.path.dirname(os.path.dirname(__file__))  # Corrected to point to the root directory

def get_current_version():
    with open(os.path.join(ADDON_DIR, "version.json"), "r") as f:
        data = json.load(f)
    return data["version"]

def get_latest_version():
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(GITHUB_REPO_URL, context=context) as response:
        data = json.loads(response.read().decode())
    return data["tag_name"]

def check_for_update():
    current_version = get_current_version()
    latest_version = get_latest_version()
    return current_version != latest_version, latest_version

def download_update(url, save_path):
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=context) as response:
        with open(save_path, "wb") as f:
            f.write(response.read())

def update_addon():
    update_available, latest_version = check_for_update()
    if update_available:
        download_url = f"https://github.com/Lokasta/ToyShowTools/archive/refs/tags/{latest_version}.zip"
        
        # Create a temporary file to save the downloaded zip
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
            save_path = tmp_file.name
            download_update(download_url, save_path)
        
        # Uninstall the existing addon
        addon_name = os.path.basename(ADDON_DIR)
        bpy.ops.preferences.addon_disable(module=addon_name)
        bpy.ops.preferences.addon_remove(module=addon_name)
        
        # Install the addon using the downloaded zip file
        try:
            bpy.ops.preferences.addon_install(filepath=save_path, overwrite=True)
            bpy.ops.preferences.addon_enable(module="toyshowtools")
        except Exception as e:
            print(f"Failed to install or enable the addon: {e}")
            return False
        
        # Delete the temporary zip file
        os.remove(save_path)
        return True
    return False

class TOYSHOWTOOLS_OT_check_for_update(bpy.types.Operator):
    bl_idname = "toyshowtools.check_for_update"
    bl_label = "Check for Update"

    def execute(self, context):
        update_available, latest_version = check_for_update()
        if update_available:
            self.report({'INFO'}, f"Update available: {latest_version}")
        else:
            self.report({'INFO'}, "No updates available.")
        return {'FINISHED'}

class TOYSHOWTOOLS_OT_update_addon(bpy.types.Operator):
    bl_idname = "toyshowtools.update_addon"
    bl_label = "Update Addon"

    def execute(self, context):
        if update_addon():
            self.report({'INFO'}, "Addon updated and reloaded successfully.")
        else:
            self.report({'INFO'}, "No updates available or failed to update.")
        return {'FINISHED'}
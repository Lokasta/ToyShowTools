import bpy
import os
import json
import urllib.request
import ssl
import tempfile
import zipfile
import shutil

# Define constants
GITHUB_API_RELEASES_URL = "https://api.github.com/repos/Lokasta/ToyShowTools/releases/latest"
ADDON_NAME = __name__.split('TOYSHOWTOOLS')[0]  # This should match your addon module name
ADDONS_DIR = bpy.utils.user_resource('SCRIPTS', "addons")
ADDON_DIR = os.path.join(ADDONS_DIR, ADDON_NAME)

def get_current_version():
    # Use bl_info['version'] as the current version
    return '.'.join(map(str, bl_info['version']))

def get_latest_version():
    context = ssl.create_default_context()
    with urllib.request.urlopen(GITHUB_API_RELEASES_URL, context=context) as response:
        data = json.loads(response.read().decode())
    return data["tag_name"]

def check_for_update():
    current_version = get_current_version()
    latest_version = get_latest_version()
    return current_version != latest_version, latest_version

def download_update(url, save_path):
    context = ssl.create_default_context()
    with urllib.request.urlopen(url, context=context) as response:
        with open(save_path, "wb") as f:
            f.write(response.read())

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def update_addon():
    update_available, latest_version = check_for_update()
    if update_available:
        download_url = f"https://github.com/Lokasta/ToyShowTools/archive/refs/tags/{latest_version}.zip"
        
        # Create a temporary directory to work in
        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, 'update.zip')
        
        # Download the update
        download_update(download_url, save_path)
        
        # Extract the zip file
        extract_zip(save_path, temp_dir)
        
        # Find the extracted directory
        extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)) and d.startswith('ToyShowTools')]
        if not extracted_dirs:
            print("No extracted directory found.")
            return False
        
        extracted_dir = os.path.join(temp_dir, extracted_dirs[0])
        
        # Backup the current addon directory
        backup_dir = ADDON_DIR + "_backup"
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.move(ADDON_DIR, backup_dir)
        
        # Move the extracted files to the addon directory
        shutil.move(extracted_dir, ADDON_DIR)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        return True
    return False

def reload_addon():
    bpy.ops.preferences.addon_disable(module=ADDON_NAME)
    bpy.ops.preferences.addon_refresh()
    bpy.ops.preferences.addon_enable(module=ADDON_NAME)

class TOYSHOWTOOLS_OT_check_for_update(bpy.types.Operator):
    bl_idname = "toyshowtools.check_for_update"
    bl_label = "Check for Update"

    def execute(self, context):
        try:
            update_available, latest_version = check_for_update()
            if update_available:
                self.report({'INFO'}, f"Update available: {latest_version}")
            else:
                self.report({'INFO'}, "No updates available.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to check for updates: {e}")
        return {'FINISHED'}

class TOYSHOWTOOLS_OT_update_addon(bpy.types.Operator):
    bl_idname = "toyshowtools.update_addon"
    bl_label = "Update Addon"

    def execute(self, context):
        try:
            if update_addon():
                self.report({'INFO'}, "Addon updated successfully. Please restart Blender.")
            else:
                self.report({'INFO'}, "No updates available or failed to update.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to update addon: {e}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(TOYSHOWTOOLS_OT_check_for_update)
    bpy.utils.register_class(TOYSHOWTOOLS_OT_update_addon)

def unregister():
    bpy.utils.unregister_class(TOYSHOWTOOLS_OT_check_for_update)
    bpy.utils.unregister_class(TOYSHOWTOOLS_OT_update_addon)
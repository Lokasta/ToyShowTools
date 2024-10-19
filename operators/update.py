import bpy
import os
import json
import urllib.request
import ssl
import tempfile
import zipfile
import shutil

GITHUB_API_RELEASES_URL = "https://api.github.com/repos/Lokasta/ToyShowTools/releases/latest"
ADDONS_DIR = os.path.join(bpy.utils.script_path_user(), "addons")
ADDON_NAME = 'ToyShowTools'  # Ensure this matches your addon folder name
ADDON_DIR = os.path.join(ADDONS_DIR, ADDON_NAME)

def get_current_version(bl_info):
    version_file = os.path.join(ADDON_DIR, "version.json")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            data = json.load(f)
        return data["version"]
    else:
        return '.'.join(map(str, bl_info['version']))

def get_latest_version():
    context = ssl.create_default_context()
    with urllib.request.urlopen(GITHUB_API_RELEASES_URL, context=context) as response:
        data = json.loads(response.read().decode())
    return data["tag_name"]

def check_for_update(bl_info):
    current_version = get_current_version(bl_info)
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
    return zip_ref.namelist()[0]

def update_addon():
    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, "update.zip")
    
    # Download the latest release
    context = ssl.create_default_context()
    with urllib.request.urlopen(GITHUB_API_RELEASES_URL, context=context) as response:
        data = json.loads(response.read().decode())
        download_url = data["zipball_url"]
        download_update(download_url, save_path)
    
    # Extract the downloaded zip file
    extracted_dir_name = extract_zip(save_path, temp_dir)
    extracted_dir = os.path.join(temp_dir, extracted_dir_name)
    
    # Replace the existing addon directory with the new one
    if os.path.exists(ADDON_DIR):
        shutil.rmtree(ADDON_DIR)
    
    shutil.move(extracted_dir, ADDON_DIR)
    
    # Clean up
    shutil.rmtree(temp_dir)
    os.remove(save_path)
    return True

def reload_addon():
    bpy.ops.preferences.addon_disable(module=ADDON_NAME)
    bpy.ops.preferences.addon_refresh()
    bpy.ops.preferences.addon_enable(module=ADDON_NAME)

class TOYSHOWTOOLS_OT_check_for_update(bpy.types.Operator):
    bl_idname = "toyshowtools.check_for_update"
    bl_label = "Check for Update"

    def execute(self, context):
        try:
            from .. import bl_info  # Import bl_info here to avoid circular import
            update_available, latest_version = check_for_update(bl_info)
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
                reload_addon()
                self.report({'INFO'}, "Addon updated successfully. Please restart Blender.")
            else:
                self.report({'INFO'}, "No updates available or failed to update.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to update addon: {e}")
        return {'FINISHED'}
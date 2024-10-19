# ToyShowTools Blender Addon

## Introduction

ToyShowTools is a Blender addon designed to streamline the setup and rendering process for animation projects. It provides tools to quickly configure project settings, render test frames, and manage output paths efficiently.

## Features

- **Project Setup**: Automatically configure project settings such as framerate, resolution, render engine, and output paths.
- **Render Test Frames**: Render frames at specified intervals and save them to a designated folder for quick previews.
- **GPU Rendering**: Automatically detect and enable GPU rendering if a compatible GPU is found.
- **Custom Output Paths**: Set custom output paths for renders, ensuring organized file management.

## Installation

1. Download the ToyShowTools addon from the repository.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click on `Install...` and select the downloaded addon file.
4. Enable the ToyShowTools addon from the list.

## Usage

### Setting Up a Project

1. Open your Blender project.
2. Save your Blender file if you haven't already.
3. Go to the `ToyShowTools` panel in the `N` sidebar.
4. Click on `Setup Project` to automatically configure the project settings.

### Rendering Test Frames

1. Open your Blender project.
2. Save your Blender file if you haven't already.
3. Go to the `ToyShowTools` panel in the `N` sidebar.
4. Set the desired frame cadency for test rendering.
5. Click on `Render Test Frames` to render frames at the specified intervals and save them to the `_RenderTestFrames` folder.

## Configuration

### Project Setup

- **Framerate**: Set to 12 fps.
- **Resolution**: Set to 1920 x 1920.
- **Render Engine**: Set to Cycles.
- **Output Path**: Set to `RENDER/filename/frame_`.

### Render Test Frames

- **Output Path**: Set to `_RenderTestFrames/filename_testframes/frame_`.
- **Resolution**: Reduced by half for faster rendering.

## Contributing

We welcome contributions to improve ToyShowTools. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your branch.
4. Create a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
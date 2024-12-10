# Blender addon to create materials with comfyui

This addon allows to create materials with AI by calling a running instance of [Comfyui](https://github.com/comfyanonymous/ComfyUI)


## Requirements

This addon requires a running instance of ComfyUI with the following requirements installed:

- A model to generate the images (`realisticVisionV51_v51VAE` by default)
- [ComfyUI-seamless-tiling](https://github.com/spinagon/ComfyUI-seamless-tiling)
- [comfy_mtb](https://github.com/melMass/comfy_mtb) (with the corresponding models)


## Usage

If you install and enable the addon, a new panel is created in the shader editor. Configure the url and model you want to use,
enter a description of the material you want to create in the `prompt` box, and click the "Generate MAterial" button.

The request will be sent to the running instance, and when iit is done, the material will be created.

bl_info = {
    "name": "ComfyUI Material Generator",
    "description": "Generate material textures with ComfyUI",
    "author": "Miguel Marco",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "category": "Material",
}

import bpy
from . import operators

def register():
    operators.register()

def unregister():
    operators.unregister()

if __name__ == "__main__":
    register()

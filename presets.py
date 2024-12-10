workflowjson = r"""
{
  "1": {
    "inputs": {
      "ckpt_name": "realisticVisionV51_v51VAE.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "2": {
    "inputs": {
      "tiling": "enable",
      "copy_model": "Make a copy",
      "model": [
        "1",
        0
      ]
    },
    "class_type": "SeamlessTile",
    "_meta": {
      "title": "Seamless Tile"
    }
  },
  "3": {
    "inputs": {
      "text": "grass and gravel texture\n",
      "clip": [
        "1",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "5": {
    "inputs": {
      "text": "",
      "clip": [
        "1",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "6": {
    "inputs": {
      "seed": 1,
      "steps": 20,
      "cfg": 4.5,
      "sampler_name": "dpmpp_2m",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "2",
        0
      ],
      "positive": [
        "3",
        0
      ],
      "negative": [
        "5",
        0
      ],
      "latent_image": [
        "7",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "7": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "12": {
    "inputs": {
      "tiling": "enable",
      "samples": [
        "6",
        0
      ],
      "vae": [
        "1",
        2
      ]
    },
    "class_type": "CircularVAEDecode",
    "_meta": {
      "title": "Circular VAE Decode (tile)"
    }
  },
  "14": {
    "inputs": {
      "images": [
        "15",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "15": {
    "inputs": {
      "mode": "Color to Normals",
      "color_to_normals_overlap": "SMALL",
      "normals_to_curvature_blur_radius": "SMALLEST",
      "normals_to_height_seamless": true,
      "image": [
        "30",
        0
      ]
    },
    "class_type": "Deep Bump (mtb)",
    "_meta": {
      "title": "Deep Bump (mtb)"
    }
  },
  "18": {
    "inputs": {
      "mode": "Normals to Height",
      "color_to_normals_overlap": "SMALL",
      "normals_to_curvature_blur_radius": "SMALLEST",
      "normals_to_height_seamless": true,
      "image": [
        "15",
        0
      ]
    },
    "class_type": "Deep Bump (mtb)",
    "_meta": {
      "title": "Deep Bump (mtb)"
    }
  },
  "19": {
    "inputs": {
      "image": [
        "18",
        0
      ]
    },
    "class_type": "ImageInvert",
    "_meta": {
      "title": "Invert Image"
    }
  },
  "22": {
    "inputs": {
      "black_level": 15.600000000000001,
      "mid_level": 25,
      "white_level": 175,
      "image": [
        "23",
        0
      ]
    },
    "class_type": "Image Levels Adjustment",
    "_meta": {
      "title": "Image Levels Adjustment"
    }
  },
  "23": {
    "inputs": {
      "contrast": 0.6,
      "brightness": 0.85,
      "IMAGE": [
        "19",
        0
      ]
    },
    "class_type": "JDC_Contrast",
    "_meta": {
      "title": "Brightness & Contrast"
    }
  },
  "24": {
    "inputs": {
      "images": [
        "27",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "27": {
    "inputs": {
      "sharpen_radius": 1,
      "sigma": 1,
      "alpha": 1,
      "image": [
        "22",
        0
      ]
    },
    "class_type": "ImageSharpen",
    "_meta": {
      "title": "ImageSharpen"
    }
  },
  "28": {
    "inputs": {
      "model_name": "OmniSR_X2_DIV2K.safetensors"
    },
    "class_type": "UpscaleModelLoader",
    "_meta": {
      "title": "Load Upscale Model"
    }
  },
  "30": {
    "inputs": {
      "upscale_model": [
        "28",
        0
      ],
      "image": [
        "12",
        0
      ]
    },
    "class_type": "ImageUpscaleWithModel",
    "_meta": {
      "title": "Upscale Image (using Model)"
    }
  },
  "34": {
    "inputs": {
      "images": [
        "30",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "53": {
    "inputs": {
      "filename_prefix": "ComfyUI_roughness",
      "images": [
        "27",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
"""

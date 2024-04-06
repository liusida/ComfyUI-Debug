def size_to_human_readable(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024**2:
        return f"{size_in_bytes / 1024:.1f} KB"
    elif size_in_bytes < 1024**3:
        return f"{size_in_bytes / 1024**2:.1f} MB"
    elif size_in_bytes < 1024**4:
        return f"{size_in_bytes / 1024**3:.1f} GB"
    else:
        return f"{size_in_bytes / 1024**4:.1f} TB"

class DebugInspectorNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string_field": ("STRING", {
                    "multiline": True, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "Connect any of the inputs to get more information."
                }),
            },
            "optional": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "vae": ("VAE",),
                "conditioning": ("CONDITIONING",),
                "latent": ("LATENT",),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "watch"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def watch(self, string_field, model=None, clip=None, vae=None, CONDITIONING=None, LATENT=None):
        results = ""
        if model:
            results += "MODEL:\n"
            results += "\tArch:\t" + model.model.latent_format.__class__.__name__ + "\n"
            results += f"\tSize:\t{size_to_human_readable(model.size)}\n"
            results += "\n"

        if clip:
            results += "CLIP:\n\n"
            results += str(type(clip.tokenizer)) + "\n"
            results += "\n"

        if vae:
            results += "VAE:\n\n"
            results += str(type(vae.first_stage_model)) + "\n"
            results += "\n"

        return { "ui": { "string_field": results } }

class DebugModelInspectorNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "output": ("STRING", {
                    "multiline": True, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "Connect any of the inputs to get more information."
                }),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "watch"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def watch(self, output, model=None):
        results = ""
        if model:
            results += "MODEL:\n"
            results += "\tArch:\t" + model.model.latent_format.__class__.__name__ + "\n"
            results += f"\tSize:\t{size_to_human_readable(model.size)}\n"
            results += "\n"

        return { "ui": { "output": results } }


# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
WEB_DIRECTORY = "./js"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "DebugInspectorNode": DebugInspectorNode,
    "DebugModelInspectorNode": DebugModelInspectorNode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "DebugInspectorNode": "Debug: Inspector",
    "DebugModelInspectorNode": "Debug: Model Inspector",
}

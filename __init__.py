import inspect
import io

def size_to_human_readable(size_in_bytes, in_bytes=True):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} "
    elif size_in_bytes < 1024**2:
        return f"{size_in_bytes / 1024:.1f} K"
    elif size_in_bytes < 1024**3:
        return f"{size_in_bytes / 1024**2:.1f} M"
    elif size_in_bytes < 1024**4:
        if in_bytes:
            return f"{size_in_bytes / 1024**3:.1f} G"
        else:
            return f"{size_in_bytes / 1024**3:.1f} B"
    else:
        return f"{size_in_bytes / 1024**4:.1f} T"

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
                    "default": ""
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
            results += "Base:\t\t" + model.model.latent_format.__class__.__name__ + "\n"
            results += f"Size:\t\t{size_to_human_readable(model.size, in_bytes=True)}B\n"
            parameter_size = sum(p.numel() for p in model.model.parameters())
            results += f"Parameters:\t{size_to_human_readable(parameter_size, in_bytes=False)}\n"

            dtype_value = model.model.get_dtype()  # Example: <class 'torch.bfloat16'>
            dtype_str = str(dtype_value).split('.')[-1]  # Split by '.' and take the last part
            print(dtype_str)  # This will print 'bfloat16'
            results += f"dtype:\t\t{dtype_str}\n"

            results += f"Model Type:\t{model.model.model_type.name}\n"

            results += "\n"

        return { "ui": { "output": results } }

class DebugModelPrintOutNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "output": ("STRING", {
                    "multiline": True, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "watch"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def watch(self, output, model=None):
        results = ""
        # Check if the model object itself exists and has the attribute 'model'
        if model and hasattr(model, 'model'):
            # Check if the 'model' attribute of the model has the attribute 'diffusion_model'
            if hasattr(model.model, 'diffusion_model'):
                # Now we can safely print the diffusion_model
                buffer = io.StringIO()
                print(model.model.diffusion_model, file=buffer)
                results += buffer.getvalue()
                buffer.close()
            else:
                results += "No diffusion_model attribute found.\n"
        else:
            results += "Model is not defined or does not have a 'model' attribute.\n"

        return { "ui": { "output": results } }


# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
WEB_DIRECTORY = "./js"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    # "DebugInspectorNode": DebugInspectorNode,
    "DebugModelInspectorNode": DebugModelInspectorNode,
    "DebugModelPrintOutNode": DebugModelPrintOutNode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    # "DebugInspectorNode": "Debug: Inspector",
    "DebugModelInspectorNode": "Debug: Model Metrics",
    "DebugModelPrintOutNode": "Debug: Model Architecture"
}

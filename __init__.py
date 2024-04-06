class DebugNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "string_field": ("STRING", {
                    "multiline": True, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "Connect any of the inputs to get more information."
                }),
            },
            "optional": {
                "MODEL": ("MODEL",),
                "CLIP": ("CLIP",),
                "VAE": ("VAE",),
                "CONDITIONING": ("CONDITIONING",),
                "LATENT": ("LATENT",),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "watch"
    OUTPUT_NODE = True
    CATEGORY = "Debug"

    def size_to_human_readable(self, size_in_bytes):
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

    def watch(self, string_field, MODEL=None, CLIP=None, VAE=None, CONDITIONING=None, LATENT=None):
        results = ""
        if MODEL:
            results += "MODEL:\n"
            results += "\tArch:\t" + MODEL.model.latent_format.__class__.__name__ + "\n"
            results += f"\tSize:\t{self.size_to_human_readable(MODEL.size)}\n"
            results += "\n"

        if CLIP:
            results += "CLIP:\n\n"
            results += str(type(CLIP.tokenizer)) + "\n"
            # results += f"size: {CLIP.size // 1024 // 1024}MB\n"
            results += "\n"

        if VAE:
            results += "VAE:\n\n"
            results += str(type(VAE.first_stage_model)) + "\n"
            # results += f"size: {VAE.size // 1024 // 1024}MB\n"
            results += "\n"

        return { "ui": { "string_field": results } }

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
WEB_DIRECTORY = "./js"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "DebugNode": DebugNode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "DebugNode": "Debug"
}

"""MidJourney diffusion client"""


from typing import final
import replicate


MODEL_NAME: final = "tstramer/midjourney-diffusion"
MODEL_VERSION: final = "436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b"


class DiffusionClient:
    """API client for replicate.com"""


    _width: int
    _height: int
    _num_outputs: int
    _prompt_strength: float
    _num_inference_steps: int
    _guidance_scale: float
    _scheduler: str


    def __init__(
            self,
            width: int,
            height: int,
            num_outputs: int = 4,
            prompt_strength: float = 0.8,
            num_inference_steps: int = 50,
            guidance_scale: float = 7.5,
            scheduler: str = "DPMSolverMultistep"
        ) -> None:
        self._width = width
        self._height = height
        self._num_outputs = num_outputs
        self._prompt_strength = prompt_strength
        self._num_inference_steps = num_inference_steps
        self._guidance_scale = guidance_scale
        self._scheduler = scheduler


    def generate(self, description: str, exclude_description: str = "") -> str:
        """Generates images and returns URL to download"""
        model = replicate.models.get(MODEL_NAME)
        version = model.versions.get(MODEL_VERSION)

        inputs = {
            'prompt': description,
            'negative_prompt': exclude_description,
            'width': self._width,
            'height': self._height,
            'prompt_strength': self._prompt_strength,
            'num_outputs': self._num_outputs,
            'num_inference_steps': self._num_inference_steps,
            'guidance_scale': self._guidance_scale,
            'scheduler': self._scheduler,
        }
        try:
            return version.predict(**inputs)
        except replicate.exceptions.ModelError:
            return version.predict(**inputs)

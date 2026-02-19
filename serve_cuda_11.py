from ray import serve
from fastapi import FastAPI
import torch
import sys
import os

app = FastAPI()

@serve.deployment(ray_actor_options={"num_cpus": 0.1})
@serve.ingress(app)
class CUDA11Check:
    @app.get("/")
    def root(self):
        return {
            "message": "Hello from CUDA 11 App",
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda,
            "python_version": sys.version,
            "env_vars": {k: v for k, v in os.environ.items() if "CUDA" in k or "NVIDIA" in k}
        }

my_app = CUDA11Check.bind()

# Prediction interface for Cog ⚙️
# https://cog.run/python

import subprocess
from cog import BasePredictor, Input, Path


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        source_image: Path = Input(description="Source image for animation"),
        driving_video: Path = Input(description="Driving video for animation"),
    ) -> Path:
        """Run a single prediction on the model"""
        image_filename = source_image.stem
        video_filename = driving_video.stem

        output_filename = f"{image_filename}--{video_filename}.mp4"
        print("output_filename------", output_filename)

        # 执行命令行程序
        cmd = [
            "python",
            "./inference_animals.py",
            "--source",
            str(source_image),
            "--driving",
            str(driving_video),
        ]

        subprocess.run(cmd, check=True)

        # 返回输出文件路径
        return Path(f"animations/{output_filename}")

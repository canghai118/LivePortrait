# coding: utf-8

"""
The entrance of animal
"""

import os
import os.path as osp
import tyro
import subprocess
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline_animal import LivePortraitPipelineAnimal


def partial_fields(target_class, kwargs):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})


def fast_check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False


def fast_check_args(args: ArgumentConfig):
    if not osp.exists(args.source):
        raise FileNotFoundError(f"source info not found: {args.source}")
    if not osp.exists(args.driving):
        raise FileNotFoundError(f"driving info not found: {args.driving}")


def main():
    # set tyro theme
    tyro.extras.set_accent_color("bright_cyan")
    args = tyro.cli(ArgumentConfig)

    # 针对动物优化默认参数
    if not hasattr(args, '_stitching_strength_set_explicitly'):
        # 如果用户没有显式设置stitching_strength，使用更适合动物的默认值
        if args.stitching_strength == 1.0:  # 如果还是默认的人脸值
            args.stitching_strength = 0.3  # 改为更适合动物的值
            print(f"🐾 Animal mode: Using stitching_strength={args.stitching_strength} (optimized for animals)")

    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    if osp.exists(ffmpeg_dir):
        os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

    if not fast_check_ffmpeg():
        raise ImportError(
            "FFmpeg is not installed. Please install FFmpeg (including ffmpeg and ffprobe) before running this script. https://ffmpeg.org/download.html"
        )

    fast_check_args(args)

    # specify configs for inference
    inference_cfg = partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = partial_fields(CropConfig, args.__dict__)

    live_portrait_pipeline_animal = LivePortraitPipelineAnimal(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg
    )

    # run
    live_portrait_pipeline_animal.execute(args)


if __name__ == "__main__":
    main()

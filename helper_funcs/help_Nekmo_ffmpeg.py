#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
import os
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from typing import List, Optional
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def place_water_mark(input_file: str, output_file: str, water_mark_file: str) -> str:
    watermarked_file = f"{output_file}.watermark.png"
    metadata = extractMetadata(createParser(input_file))
    width = metadata.get("width")
    shrink_watermark_file_generator_command = [
        "ffmpeg",
        "-i", water_mark_file,
        "-y", "-v", "quiet",
        "-vf", f"scale={width}*0.5:-1",
        watermarked_file
    ]
    process = await asyncio.create_subprocess_exec(
        *shrink_watermark_file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
    except asyncio.TimeoutError:
        process.kill()
        logger.error("Subprocess took too long, killing it")
        stdout, stderr = b"", b""
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.exists(watermarked_file):
        commands_to_execute = [
            "ffmpeg",
            "-i", input_file,
            "-i", watermarked_file,
            "-filter_complex",
            "overlay=(main_w-overlay_w):(main_h-overlay_h)",
            output_file
        ]
        process = await asyncio.create_subprocess_exec(
            *commands_to_execute,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
        except asyncio.TimeoutError:
            process.kill()
            logger.error("Subprocess took too long, killing it")
            stdout, stderr = b"", b""
        e_response += stderr.decode().strip()
        t_response += stdout.decode().strip()
        if os.path.exists(output_file):
            return output_file
    logger.error(f"Error processing watermark: {e_response}")
    return None

async def take_screen_shot(video_file: str, output_directory: str, ttl: float) -> Optional[str]:
    out_put_file_name = os.path.join(output_directory, f"{int(time.time())}.jpg")
    file_generator_command = [
        "ffmpeg",
        "-ss", str(ttl),
        "-i", video_file,
        "-vframes", "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
    except asyncio.TimeoutError:
        process.kill()
        logger.error("Subprocess took too long, killing it")
        stdout, stderr = b"", b""
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.exists(out_put_file_name):
        return out_put_file_name
    logger.error(f"Error taking screenshot: {e_response}")
    return None

async def cut_small_video(video_file: str, output_directory: str, start_time: str, end_time: str) -> Optional[str]:
    out_put_file_name = os.path.join(output_directory, f"{int(time.time())}.mp4")
    file_generator_command = [
        "ffmpeg",
        "-i", video_file,
        "-ss", start_time,
        "-to", end_time,
        "-async", "1",
        "-strict", "-2",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
    except asyncio.TimeoutError:
        process.kill()
        logger.error("Subprocess took too long, killing it")
        stdout, stderr = b"", b""
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.exists(out_put_file_name):
        return out_put_file_name
    logger.error(f"Error cutting video: {e_response}")
    return

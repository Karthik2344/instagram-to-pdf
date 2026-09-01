# instagram_downloader.py

import instaloader
import requests
from pathlib import Path


def extract_shortcode(url):
    url = url.rstrip("/")

    parts = url.split("/")

    if "p" not in parts:
        raise ValueError("Invalid Instagram post URL")

    p_index = parts.index("p")

    if p_index + 1 >= len(parts):
        raise ValueError("Invalid Instagram post URL")

    return parts[p_index + 1]


def download_post(url, output_folder):

    shortcode = extract_shortcode(url)

    loader = instaloader.Instaloader()

    post = instaloader.Post.from_shortcode(
        loader.context,
        shortcode
    )

    downloaded_files = []

    if post.typename == "GraphSidecar":

        for index, node in enumerate(
            post.get_sidecar_nodes(),
            start=1
        ):

            if node.is_video:
                continue

            response = requests.get(
                node.display_url,
                timeout=30
            )

            response.raise_for_status()

            filename = (
                Path(output_folder)
                / f"{index:02d}.jpg"
            )

            filename.write_bytes(response.content)

            downloaded_files.append(filename)

    else:

        if post.is_video:
            raise ValueError(
                "This post contains a video."
            )

        response = requests.get(
            post.url,
            timeout=30
        )

        response.raise_for_status()

        filename = (
            Path(output_folder)
            / "01.jpg"
        )

        filename.write_bytes(response.content)

        downloaded_files.append(filename)

    return downloaded_files
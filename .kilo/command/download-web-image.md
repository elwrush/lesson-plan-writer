---
description: Download an image from a URL (HTTP/HTTPS or data: URI), validate resolution, compress for slide use, and save to the specified output path.
---

# Command: Download Web Image

## Usage
`/download-web-image <url> [output_path]`

- **url** (required) — direct image URL or data: URI
- **output_path** (required if url is the only arg) — full destination path, e.g. `output/{subfolder}/slides/assets/my_image.jpg`

If `output_path` is omitted you will be prompted for it.

## What it does
1. Loads the `download-image-from-url` global skill
2. Fetches/decodes the image from the URL
3. **Validates resolution** against the 1280x720 minimum (full-bleed slide background use assumed). If below minimum, warns with dimensions and confirms before proceeding.
4. Compresses via Pillow (JPEG quality=80, max 1920px edge)
5. Saves to the specified output path
6. Prints the saved file path, dimensions, and size

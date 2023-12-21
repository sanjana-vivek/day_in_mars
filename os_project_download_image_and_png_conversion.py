import os
import urllib3
from PIL import Image
from io import BytesIO
import magic
from urllib.parse import urlparse

def download_and_convert_to_png(image_url, output_folder='.'):
    # Create a connection pool for downloading
    http = urllib3.PoolManager()

    # Download the image
    response = http.request('GET', image_url, preload_content=False)

    # Extract the server filename from the Content-Disposition header
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        _, params = cgi.parse_header(content_disposition)
        server_filename = params.get('filename')
    else:
        # If Content-Disposition header is not present, extract filename from URL
        parsed_url = urlparse(image_url)
        server_filename = os.path.basename(parsed_url.path)

    # Determine the file type using magic bytes
    mime_type = magic.Magic()
    file_type = mime_type.from_buffer(response.data)

    # Check if the image is in JPG format
    if file_type.startswith('image/jpeg') or 'JPEG' in file_type:
        # Convert JPG to PNG
        image = Image.open(BytesIO(response.data))
        png_path = os.path.join(output_folder, os.path.splitext(server_filename)[0] + '.png')
        image.save(png_path, format='PNG')
    elif file_type.startswith('image/png') or "PNG" in file_type:
        # Save the PNG image directly
        png_path = os.path.join(output_folder, server_filename)
        with open(png_path, 'wb') as png_file:
            png_file.write(response.data)
    else:
        raise ValueError(f"Unsupported image format {file_type}. Supported formats: JPG/JPEG, PNG")

    return png_path
'''# Example usage:
image_url = 'https://media.licdn.com/dms/image/sync/D5610AQFuA1f3MQ7wbw/image-shrink_800/0/1696872498671/LI-ondajpg?e=1700838000&v=beta&t=HK1h9KcJ4-fSt6-oUjcIJ05tF-O7XAoycgOhtCmUJE0'
output_path = download_and_convert_to_png(image_url)
print(f"The converted image is saved at: {output_path}")
'''
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import os

def csv_to_image(data):
    """
    Convert a CSV data frame to a grayscale image array.

    Args:
        data (pandas.DataFrame): The input CSV data frame.

    Returns:
        numpy.ndarray: The grayscale image array.
    """
    image_array = data.iloc[:, 1:].values
    image_array = np.nan_to_num(image_array)  # Replace NaN with zero
    min_val = np.min(image_array)
    max_val = np.max(image_array)
    if min_val == max_val:
        return np.zeros_like(image_array, dtype=np.uint8)
    image_array = ((image_array - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    return image_array

def resize_image(image_array, new_width=150):
    """
    Resize an image array while maintaining the aspect ratio.

    Args:
        image_array (numpy.ndarray): The input image array.
        new_width (int): The desired width of the resized image.

    Returns:
        numpy.ndarray: The resized image array.
    """
    image = Image.fromarray(image_array)
    width_percent = (new_width / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percent)))
    new_image = image.resize((new_width, new_height), Image.LANCZOS)
    return np.array(new_image)

def apply_custom_colormap(full_image, depth_min, depth_max):
    """
    Apply a custom colormap to a specific depth range of an image.

    Args:
        full_image (numpy.ndarray): The input image array.
        depth_min (int): The minimum depth value to apply the colormap.
        depth_max (int): The maximum depth value to apply the colormap.

    Returns:
        numpy.ndarray: The image array with the custom colormap applied.
    """
    plt.figure(figsize=(10, full_image.shape[0]/10))
    
    # Ensure full_image is 2D
    if full_image.ndim == 3:
        full_image = full_image[:,:,0]  # Take the first channel if it's RGB
    
    # Create a copy of the full image and convert to RGB
    colored_image = np.stack((full_image,)*3, axis=-1)
    
    # Apply colormap only to the selected depth range
    colored_slice = plt.cm.viridis(full_image[depth_min:depth_max+1] / 255.0)
    
    # Convert the colored slice to 8-bit RGB
    colored_slice_rgb = (colored_slice[:, :, :3] * 255).astype(np.uint8)
    
    # Insert the colored slice back into the full image
    colored_image[depth_min:depth_max+1] = colored_slice_rgb
    
    plt.imshow(colored_image, aspect='auto')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig('temp_colored_image.png', bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()
    
    colored_image = Image.open('temp_colored_image.png')
    os.remove('temp_colored_image.png')  # Clean up the temporary file
    return np.array(colored_image)

def save_image(image_array, depth, folder):
    """
    Save an image array to a file.

    Args:
        image_array (numpy.ndarray): The input image array.
        depth (str): The depth information to include in the filename.
        folder (str): The folder path to save the image.

    Returns:
        None
    """
    os.makedirs(folder, exist_ok=True)
    image = Image.fromarray(image_array.astype('uint8'))
    if depth == 'original':
        image.save(os.path.join(folder, f'depth_original.png'))
    else:
        image.save(os.path.join(folder, f'depth_{depth}.png'))
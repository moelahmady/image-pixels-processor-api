from flask import request, jsonify, Blueprint, send_file
from sqlalchemy.orm import Session
from sqlalchemy import delete
from .database import get_db, Image
from .image_processing import resize_image, apply_custom_colormap, save_image, csv_to_image
import pandas as pd
import io
from PIL import Image as PILImage
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

def configure_routes(app):
    """
    Configure routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/process_image', methods=['POST'])
    def process_images():
        """
        Process and save an image to the database.

        Returns:
            JSON response indicating the success or failure of the image processing.
        """

        # Read the CSV data
        data = pd.read_csv(os.getenv('CSV_IMAGE_PATH'))
        db = next(get_db())

        print("Starting image processing...")

        # Delete all existing records from the database
        db.execute(delete(Image))
        db.commit()
        print("Deleted existing records from the database.")

        # Convert CSV to a single image
        image_array = csv_to_image(data)

        # Resize the image
        resized_image = resize_image(image_array, new_width=150)

        # Save resized image to the database as binary
        img = PILImage.fromarray(resized_image)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        # Create a new image entry and save it to the database
        image_entry = Image(depth=0, path='full_image.png')
        image_entry.image_data = img_byte_array

        db.add(image_entry)
        db.commit()
        print("Image processed and saved to the database successfully.")
        return jsonify({'message': 'Image processed and saved successfully'})

    @app.route('/get_frames', methods=['GET'])
    def get_images():
        """
        Retrieve and process images based on the provided depth range.

        Returns:
            JSON response containing the paths to the original and colored images.
        """

        # Get the depth range from the request parameters
        depth_min = request.args.get('depth_min', type=int)
        depth_max = request.args.get('depth_max', type=int)

        # Check if depth_min and depth_max are provided
        if depth_min is None or depth_max is None:
            return jsonify({'error': 'depth_min and depth_max must be provided'}), 400

        # Check if depth_min is less than or equal to depth_max
        if depth_min > depth_max:
            return jsonify({'error': 'depth_min must be less than or equal to depth_max'}), 400

        db = next(get_db())
        image = db.query(Image).first()  # Get the single image from the database

        if image:
            try:
                # Open the image from the database and convert it to an array
                img = PILImage.open(io.BytesIO(image.image_data))
                img_array = np.array(img)

                # Check if the requested depth range is valid
                if depth_max >= img_array.shape[0]:
                    return jsonify({'error': f'depth_max ({depth_max}) is out of range. Max depth is {img_array.shape[0] - 1}'}), 400

                # Save the original image
                save_image(img_array, 'original', 'original_images')
                original_image_path = f'/{os.getenv('OUTPUT_DIR')}/original_images/depth_original.png'

                # Apply colormap and save the colored image
                colored_image = apply_custom_colormap(img_array, depth_min, depth_max)
                save_image(colored_image, f'{depth_min}_{depth_max}', 'colored_images')
                colored_image_path =  f'/{os.getenv('OUTPUT_DIR')}/colored_images/depth_{depth_min}_{depth_max}.png'

                print(f"Saved original image and applied color map for depths {depth_min} to {depth_max}")

                return jsonify({
                    'original_image': original_image_path,
                    'colored_image': colored_image_path
                })
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                return jsonify({'error': 'Error processing image'}), 500
        else:
            return jsonify({'error': 'Image not found in database'}), 404

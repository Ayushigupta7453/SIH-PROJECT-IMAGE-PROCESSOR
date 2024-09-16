# app/routes.py
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db_connection
from app.utils import process_image

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', processed=False)

@main.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No image file found')
        return redirect(url_for('main.index'))

    image_file = request.files['image']
    if image_file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.index'))

    if image_file:
        # Save original image
        image_path = os.path.join('app/static/uploads', image_file.filename)
        image_file.save(image_path)
        
        # Process image and calculate SNR
        snr_before, snr_after, enhanced_image_path = process_image(image_path)
        
        # Save results to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO image_results (image_path, snr_before, snr_after) VALUES (%s, %s, %s)',
            (image_path, snr_before, snr_after)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Extract filenames to pass to the template
        original_image_filename = os.path.basename(image_path)
        enhanced_image_filename = os.path.basename(enhanced_image_path)

        flash('Image uploaded and processed successfully!')
        return render_template('index.html', 
                               processed=True, 
                               snr_before=snr_before, 
                               snr_after=snr_after,
                               original_image_filename=original_image_filename,
                               enhanced_image_filename=enhanced_image_filename)
    
    flash('Invalid file format')
    return redirect(url_for('main.index'))

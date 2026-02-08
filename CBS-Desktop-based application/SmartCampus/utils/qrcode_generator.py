"""
QR Code Generator Utility
"""

import qrcode
import os
from datetime import datetime


class QRCodeGenerator:
    """Generate QR codes for classrooms and resources"""
    
    @staticmethod
    def generate_classroom_qr(classroom_id, room_number, building, capacity):
        """Generate QR code for a classroom"""
        try:
            # Create QR code data
            qr_data = f"Classroom:{room_number}|Building:{building}|Capacity:{capacity}|ID:{classroom_id}"
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            return img
        except Exception as e:
            print(f"QR code generation error: {e}")
            return None
    
    @staticmethod
    def save_qr_code(image, filename):
        """Save QR code image to file"""
        try:
            # Create directory if it doesn't exist
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            qr_dir = os.path.join(base_path, "qr_codes")
            os.makedirs(qr_dir, exist_ok=True)
            
            filepath = os.path.join(qr_dir, filename)
            image.save(filepath)
            
            return filepath
        except Exception as e:
            print(f"Save QR code error: {e}")
            return None
    
    @staticmethod
    def generate_and_save_qr(classroom_id, room_number, building, capacity):
        """Generate and save QR code in one step"""
        try:
            img = QRCodeGenerator.generate_classroom_qr(classroom_id, room_number, building, capacity)
            if img:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"classroom_{room_number}_{timestamp}.png"
                filepath = QRCodeGenerator.save_qr_code(img, filename)
                return filepath
            return None
        except Exception as e:
            print(f"Generate and save QR error: {e}")
            return None

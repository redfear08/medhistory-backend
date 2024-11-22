import qrcode
import os

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("\n".join(data))
    qr.make(fit=True)

    qr_code_path = 'static/uploads/medical_history_qr.png'
    os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
    qr.make_image(fill_color="black", back_color="white").save(qr_code_path)
    return qr_code_path

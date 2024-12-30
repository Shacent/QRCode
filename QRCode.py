import streamlit as st
import qrcode
import segno
from io import BytesIO
import base64
from PIL import Image

def generate_qr_code(data):
    """Generate a QR code image in PNG format."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def pil_to_bytes(img):
    """Convert a PIL Image to bytes."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    return buffered.getvalue()

def generate_svg_qr_code(data):
    """Generate a QR code in SVG format."""
    qr = segno.make(data)
    buffer = BytesIO()
    qr.save(buffer, kind='svg')
    buffer.seek(0)
    return buffer.getvalue()

def get_download_button(file_data, file_format, filename):
    """Create a styled download button."""
    b64 = base64.b64encode(file_data).decode()
    mime_type = "image/png" if file_format == "PNG" else "image/svg+xml"
    return f"""
        <a href="data:{mime_type};base64,{b64}" download="{filename}" style="
            display: inline-block;
            text-decoration: none;
            padding: 10px 20px;
            color: white;
            background-color: #4CAF50;
            border-radius: 5px;
            font-size: 16px;
            text-align: center;
            margin: 5px;
            width: 150px;
            text-align: center;
        ">Download as {file_format}</a>
    """

# Streamlit UI
st.title("QR Code Generator")

# Input field for the link
link = st.text_input("Enter the link you want to generate a QR code for:")

if link:
    # Generate the QR Code in PNG
    qr_image = generate_qr_code(link)

    # Convert QR Code to bytes for Streamlit
    qr_image_bytes = pil_to_bytes(qr_image)

    # Generate the QR Code in SVG
    qr_svg = generate_svg_qr_code(link)

    # Display QR Code Preview with smaller size and center it
    st.markdown(
        f'<div style="text-align: center;">'
        f'<img src="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode()}" width="400">'
        f'</div>',
        unsafe_allow_html=True
    )

    # Display styled download buttons side by side
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; gap: 10px;">
            {get_download_button(qr_image_bytes, "PNG", "qr_code.png")}
            {get_download_button(qr_svg, "SVG", "qr_code.svg")}
        </div>
        """,
        unsafe_allow_html=True,
    )

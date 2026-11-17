"""Interactive Streamlit interface for VisionForge AI."""

from __future__ import annotations

import io

import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="VisionForge AI", page_icon="🔎", layout="wide")

st.title("VisionForge AI")
st.caption("An interactive computer-vision workbench powered by OpenCV.")
st.write("Upload an image, choose an operation, adjust its parameters, and download the result.")

uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "bmp", "webp"])

if uploaded is None:
    st.info("Upload an image to get started. Your image is processed in this session and is not uploaded to a VisionForge server.")
    st.stop()

raw = np.frombuffer(uploaded.getvalue(), dtype=np.uint8)
image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
if image is None:
    st.error("OpenCV could not read this file. Try a valid PNG, JPEG, BMP, or WebP image.")
    st.stop()

height, width = image.shape[:2]
left, right = st.columns(2)
with left:
    st.subheader("Original")
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_container_width=True)
    st.caption(f"{width} × {height} pixels · {uploaded.type or 'image'}")
with right:
    st.subheader("Processed result")
    operation = st.selectbox(
        "Operation",
        ["Grayscale", "Canny edges", "Gaussian blur", "Sharpen", "Binary threshold", "RGB histogram"],
    )

    if operation == "Canny edges":
        low = st.slider("Lower threshold", 0, 255, 100)
        high = st.slider("Upper threshold", 0, 255, 200)
        if low >= high:
            st.warning("The upper threshold should be greater than the lower threshold.")
            st.stop()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        softened = cv2.GaussianBlur(gray, (5, 5), 0)
        result = cv2.Canny(softened, low, high)
        preview = result
    elif operation == "Grayscale":
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        preview = result
    elif operation == "Gaussian blur":
        strength = st.slider("Blur strength", 1, 25, 5, step=2)
        result = cv2.GaussianBlur(image, (strength, strength), 0)
        preview = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    elif operation == "Sharpen":
        strength = st.slider("Sharpen strength", 0.5, 3.0, 1.0, step=0.25)
        blurred = cv2.GaussianBlur(image, (0, 0), 3)
        result = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
        preview = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    elif operation == "Binary threshold":
        threshold = st.slider("Threshold", 0, 255, 127)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        preview = result
    else:
        colors = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        histogram = np.zeros((300, 512, 3), dtype=np.uint8)
        for channel, color in enumerate(((255, 0, 0), (0, 255, 0), (0, 0, 255))):
            values = cv2.calcHist([colors], [channel], None, [256], [0, 256])
            cv2.normalize(values, values, 0, 280, cv2.NORM_MINMAX)
            points = np.int32(np.column_stack((np.arange(256) * 2, 299 - values.ravel())))
            cv2.polylines(histogram, [points], False, color, 2)
        result = cv2.cvtColor(histogram, cv2.COLOR_RGB2BGR)
        preview = histogram

    st.image(preview, use_container_width=True)
    output = io.BytesIO()
    Image.fromarray(result if result.ndim == 2 else cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(output, format="PNG")
    st.download_button(
        "Download result as PNG",
        data=output.getvalue(),
        file_name="visionforge-result.png",
        mime="image/png",
        use_container_width=True,
    )

with st.expander("Image details"):
    st.json(
        {
            "filename": uploaded.name,
            "width": width,
            "height": height,
            "channels": int(image.shape[2]),
            "file_size_bytes": len(uploaded.getvalue()),
            "operation": operation,
        }
    )

st.caption("VisionForge AI · Classical image processing runs locally in this Streamlit process. Results depend on image content and selected parameters.")

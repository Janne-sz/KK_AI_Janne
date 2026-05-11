import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from scipy import ndimage
from streamlit_drawable_canvas import st_canvas


# MODEL_PATH = "mnist_tuned_cnn.keras" # För lokal tester
# MODEL_PATH = "streamlit-digit-demo-deploy/mnist_tuned_cnn.keras" # Från streamlit-foldern i github

import os

# Hitta mappen där app.py ligger
current_dir = os.path.dirname(__file__)
MODEL_PATH = os.path.join(current_dir, "mnist_tuned_cnn.keras")

@st.cache_resource
def load_digit_model():
    return tf.keras.models.load_model(MODEL_PATH)


def preprocess_canvas_image(image_data):
    """Convert the canvas RGBA image to MNIST-like shape (1, 28, 28, 1)."""
    if image_data is None:
        return None, None

    image = Image.fromarray(image_data.astype("uint8")).convert("L")
    pixels = np.asarray(image).astype("float32") / 255.0

    # The canvas is configured as white strokes on black background.
    mask = pixels > 0.05
    if not mask.any():
        return None, None

    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    cropped = pixels[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]

    height, width = cropped.shape
    scale = 20.0 / max(height, width)
    new_width = max(1, int(round(width * scale)))
    new_height = max(1, int(round(height * scale)))

    cropped_image = Image.fromarray((cropped * 255).astype("uint8"))
    resized = cropped_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_pixels = np.asarray(resized).astype("float32") / 255.0

    mnist = np.zeros((28, 28), dtype="float32")
    top = (28 - new_height) // 2
    left = (28 - new_width) // 2
    mnist[top : top + new_height, left : left + new_width] = resized_pixels

    center_y, center_x = ndimage.center_of_mass(mnist)
    if not np.isnan(center_y) and not np.isnan(center_x):
        shift_y = 13.5 - center_y
        shift_x = 13.5 - center_x
        mnist = ndimage.shift(mnist, shift=(shift_y, shift_x), order=1, mode="constant", cval=0.0)

    mnist = np.clip(mnist, 0.0, 1.0)
    model_input = mnist.reshape(1, 28, 28, 1)
    return model_input, mnist


def reset_prediction():
    st.session_state.canvas_version += 1
    st.session_state.predicted_digit = None
    st.session_state.confidence = None
    st.session_state.preview_image = None


st.set_page_config(page_title="Sifferprediktion", page_icon="0", layout="centered")
st.markdown(
    """
    <style>
    #MainMenu,
    header,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 280px;
        padding-top: 0.75rem;
        padding-left: 0;
        padding-right: 0;
    }

    .app-header h1 {
        text-align: center;
        font-size: 1.75rem;
        margin: 0 0 0.75rem 0;
        padding: 0;
        line-height: 1.15;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #16803c;
        border-color: #16803c;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #10652f;
        border-color: #10652f;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #1f67d2;
        border-color: #1f67d2;
        color: #ffffff;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #1854ad;
        border-color: #1854ad;
        color: #ffffff;
    }

    div[data-testid="stExpander"] {
        max-width: 280px;
    }

    div[data-testid="stMetric"] {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0
if "predicted_digit" not in st.session_state:
    st.session_state.predicted_digit = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None
if "preview_image" not in st.session_state:
    st.session_state.preview_image = None

st.markdown(
    """
    <div class="app-header">
        <h1>Sifferprediktion</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

canvas_result = st_canvas(
    stroke_width=18,
    stroke_color="#FFFFFF",
    background_color="#000000",
    height=280,
    width=280,
    drawing_mode="freedraw",
    display_toolbar=False,
    key=f"canvas_{st.session_state.canvas_version}",
)

has_result = st.session_state.predicted_digit is not None

if not has_result:
    predict_clicked = st.button(
        "Rita en siffra i rutan - tryck sen h\u00e4r",
        type="primary",
        use_container_width=True,
    )

    if predict_clicked:
        model_input, preview_image = preprocess_canvas_image(canvas_result.image_data)

        if model_input is None:
            st.warning("Rita en siffra f\u00f6rst.")
        else:
            model = load_digit_model()
            prediction = model.predict(model_input, verbose=0)[0]
            st.session_state.predicted_digit = int(np.argmax(prediction))
            st.session_state.confidence = float(np.max(prediction))
            st.session_state.preview_image = preview_image
            st.rerun()

else:
    result_col, confidence_col = st.columns(2)
    result_col.metric("Prediktion", st.session_state.predicted_digit)
    confidence_col.metric("Konfidens", f"{st.session_state.confidence:.2f}")

    if st.button("Ny siffra", use_container_width=True):
        reset_prediction()
        st.rerun()

    with st.expander("Visa preprocessad 28x28-bild"):
        st.image(st.session_state.preview_image, width=140, clamp=True)


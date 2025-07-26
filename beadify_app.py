import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io

st.set_page_config(page_title="Beadify App", layout="wide")

st.title("🎨 Beadify Your Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
bead_resolution = st.slider("Adjust bead resolution (lower = finer detail)", 5, 100, 30)

def resize_image(image, scale):
    width, height = image.size
    new_size = (width // scale, height // scale)
    return image.resize(new_size, Image.NEAREST)

def kmeans_beadify(image_array, n_colors=12):
    w, h, d = image_array.shape
    flat_img = image_array.reshape((w * h, d))
    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(flat_img)
    clustered = kmeans.cluster_centers_[kmeans.labels_]
    clustered_img = clustered.reshape((w, h, d)).astype(np.uint8)
    return clustered_img

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    
    # Resize to low resolution (bead resolution)
    bead_image = resize_image(image, bead_resolution)

    # Convert back to numpy and cluster
    bead_np = np.array(bead_image)
    clustered = kmeans_beadify(bead_np)

    # Convert back to image for final render
    final_img = Image.fromarray(clustered).resize(image.size, Image.NEAREST)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_column_width=True)
    with col2:
        st.subheader("Beadified Image")
        st.image(final_img, use_column_width=True)

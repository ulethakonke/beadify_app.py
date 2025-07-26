import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# --- Settings ---
NUM_STRINGS = 2600   # Horizontal resolution (number of bead lines)
NUM_BEADS = 600      # Vertical resolution (number of beads per string)
NUM_COLORS = 20      # Limit to 20 bead colors

st.title("🎨 Beadify: Convert Images to Beadwork")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load and resize image
    img = Image.open(uploaded_file)
    img = img.convert('RGB')
    img_resized = img.resize((NUM_STRINGS, NUM_BEADS))
    img_array = np.array(img_resized).reshape(-1, 3)

    # K-means color reduction
    kmeans = KMeans(n_clusters=NUM_COLORS, random_state=0).fit(img_array)
    labels = kmeans.predict(img_array)
    bead_palette = kmeans.cluster_centers_.astype(int)

    # Reconstruct image with bead palette
    bead_img_array = bead_palette[labels].reshape((NUM_BEADS, NUM_STRINGS, 3)).astype(np.uint8)
    bead_img = Image.fromarray(bead_img_array)

    # Display original & beadified version
    st.subheader("Original Image (resized)")
    st.image(img_resized, use_column_width=True)

    st.subheader("Bead Layout Preview")
    st.image(bead_img, use_column_width=True)

    # Option to download bead image
    st.download_button(
        label="Download Bead Image",
        data=bead_img.tobytes(),
        file_name="bead_image.bmp",
        mime="image/bmp"
    )

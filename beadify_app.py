import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Beadify Image", layout="centered")
st.title("🎨 Beadify Your Image!")
st.markdown("Convert any image into a bead-art grid. Upload a photo and choose how many bead colors you'd like to use.")

# Upload image
uploaded_file = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])

# Configurable settings
num_colors = st.slider("Number of bead colors", min_value=2, max_value=50, value=15)
output_size = st.slider("Bead grid width (pixels)", min_value=20, max_value=200, value=50)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((output_size, int(image.height * output_size / image.width)))

    # Flatten image and apply KMeans clustering
    image_np = np.array(image)
    flat_img = image_np.reshape(-1, 3)

    st.text("Reducing image to bead palette...")
    kmeans = KMeans(n_clusters=num_colors, random_state=42).fit(flat_img)
    clustered = kmeans.cluster_centers_[kmeans.labels_].astype("uint8").reshape(image_np.shape)

    # Show final bead-style image
    st.subheader("🧵 Beadified Output")
    st.image(clustered, caption="Bead-style Output", use_column_width=True)

    # Show pixel color map
    st.subheader("🧷 Bead Color Palette")
    palette = np.array(kmeans.cluster_centers_).astype("uint8")
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.imshow([palette])
    ax.axis("off")
    st.pyplot(fig)

    # Download image
    result = Image.fromarray(clustered)
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    st.download_button("⬇️ Download Beadified Image", data=buf.getvalue(), file_name="beadified.png", mime="image/png")

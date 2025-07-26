import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import numpy as np

st.set_page_config(layout="wide")
st.title("🧵 Beadify - Convert Image to Beaded Art Preview")

# Sidebar controls
st.sidebar.header("🔧 Settings")
bead_diameter = st.sidebar.slider("Bead Size (mm)", 2, 20, 5)
bead_spacing = st.sidebar.slider("Spacing Between Beads (pixels)", 0, 10, 2)
max_strings = st.sidebar.slider("Number of Bead Strings (Width)", 30, 200, 100)
shiny = st.sidebar.checkbox("Add Shine to Beads", value=True)

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_ratio = img.height / img.width

    # Resize the image to fit the number of bead strings
    img = img.resize((max_strings, int(max_strings * img_ratio)))
    colors = np.array(img)

    rows, cols = colors.shape[0], colors.shape[1]
    bead_img = Image.new("RGB", ((bead_diameter + bead_spacing) * cols, (bead_diameter + bead_spacing) * rows), "white")
    draw = ImageDraw.Draw(bead_img)

    for y in range(rows):
        for x in range(cols):
            color = tuple(colors[y, x])
            cx = x * (bead_diameter + bead_spacing) + bead_diameter // 2
            cy = y * (bead_diameter + bead_spacing) + bead_diameter // 2
            bbox = [
                (cx - bead_diameter // 2, cy - bead_diameter // 2),
                (cx + bead_diameter // 2, cy + bead_diameter // 2)
            ]
            draw.ellipse(bbox, fill=color)

            if shiny:
                shine_x = cx - bead_diameter // 4
                shine_y = cy - bead_diameter // 4
                shine_radius = bead_diameter // 6
                draw.ellipse([
                    (shine_x, shine_y),
                    (shine_x + shine_radius, shine_y + shine_radius)
                ], fill="white")

    # Show final result
    st.image(bead_img, caption="🧵 Beadified Preview", use_column_width=True)
    st.download_button("Download Beaded Image", data=bead_img.tobytes(), file_name="beaded_art.png")

else:
    st.info("📷 Upload an image to get started.")


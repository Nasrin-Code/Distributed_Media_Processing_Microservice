import streamlit as st

st.set_page_config(
    page_title="Distributed Media Processor",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Distributed Media Processor")
st.write("Upload your media and select a processing operation.")

st.subheader("Upload Media")

uploaded_file = st.file_uploader(
    "Choose an image or video file",
    type=["jpg", "jpeg", "png", "mp4", "avi", "mov"],
)

operation = st.selectbox(
    "Select Operation",
    [
        "Image Resize",
        "Image Crop",
        "Image Compression",
        "Video Thumbnail",
        "Video Transcode",
    ],
)

if uploaded_file:
    st.success(f"Selected file: {uploaded_file.name}")

if st.button("Process Media"):
    if uploaded_file is None:
        st.warning("Upload a media file first.")
    else:
        st.info("Processing request will be connected to the FastAPI backend next.")
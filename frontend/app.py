
import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Distributed Media Processor",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Distributed Media Processor")
st.write("Upload a video, process it, and monitor its status.")

uploaded_file = st.file_uploader(
    "Choose a video file",
    type=["mp4", "avi", "mov"],
)

operation_labels = {
    "Video Transcoding": "transcode",
    "Thumbnail Extraction": "thumbnail",
}

selected_operation = st.selectbox(
    "Select an operation",
    list(operation_labels.keys()),
)

if st.button("Upload and Process", type="primary"):
    if uploaded_file is None:
        st.warning("Choose a video file first.")
    else:
        try:
            with st.spinner("Uploading video..."):
                upload_response = requests.post(
                    f"{API_URL}/upload",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type or "application/octet-stream",
                        )
                    },
                    timeout=120,
                )
                upload_response.raise_for_status()

            with st.spinner("Submitting processing job..."):
                job_response = requests.post(
                    f"{API_URL}/jobs",
                    json={
                        "filename": upload_response.json()["filename"],
                        "operation": operation_labels[selected_operation],
                    },
                    timeout=15,
                )
                job_response.raise_for_status()

            job = job_response.json()
            st.session_state["job_id"] = job["job_id"]
            st.session_state["job_status"] = job["status"]
            st.success("Video uploaded and processing job submitted!")

        except requests.RequestException as error:
            st.error(f"Request failed: {error}")

if "job_id" in st.session_state:
    st.subheader("Job Status")
    st.write(f"Job ID: `{st.session_state['job_id']}`")
    st.write(f"Current status: **{st.session_state['job_status']}**")

    if st.button("Refresh Job Status"):
        try:
            response = requests.get(
                f"{API_URL}/jobs/{st.session_state['job_id']}",
                timeout=15,
            )
            response.raise_for_status()
            st.session_state["job_status"] = response.json()["status"]
            st.rerun()
        except requests.RequestException as error:
            st.error(f"Could not retrieve job status: {error}")

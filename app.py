import streamlit as st
import tempfile
from pathlib import Path

from instagram_downloader import download_post
from pdf_creator import create_pdf

st.set_page_config(page_title="Instagram → PDF", page_icon="📚", layout="centered")


# -----------------------------
# Header
# -----------------------------

st.title("📚 Instagram → PDF")

st.write("Convert an Instagram post or carousel " "into a single PDF.")


# -----------------------------
# Input
# -----------------------------

url = st.text_input("Instagram Post URL", placeholder="https://www.instagram.com/p/...")


pdf_name = st.text_input("PDF Name", value="Instagram_Notes")


# -----------------------------
# Convert button
# -----------------------------

if st.button("Convert to PDF", type="primary", use_container_width=True):

    if not url:
        st.warning("Please enter an Instagram post URL.")

    else:

        with st.spinner("Fetching Instagram post..."):

            try:

                # Temporary working directory
                with tempfile.TemporaryDirectory() as temp_dir:

                    image_folder = Path(temp_dir) / "images"

                    image_folder.mkdir()

                    # Download images
                    images = download_post(url, image_folder)

                    if not images:

                        st.error("No images were found.")

                    else:

                        st.success(f"{len(images)} image(s) found!")

                        # Show preview
                        st.subheader("Preview")

                        cols = st.columns(min(len(images), 4))

                        for i, image in enumerate(images):

                            with cols[i % len(cols)]:

                                st.image(str(image), use_container_width=True)

                        # Create PDF
                        pdf_path = Path(temp_dir) / f"{pdf_name}.pdf"

                        create_pdf(images, pdf_path)

                        # Read PDF
                        pdf_bytes = pdf_path.read_bytes()

                        st.success("PDF created successfully! 🎉")

                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=f"{pdf_name}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

            except Exception as e:

                st.error(f"Something went wrong: {e}")

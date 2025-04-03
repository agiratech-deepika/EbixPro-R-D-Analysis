import streamlit as st
from controllers.scraper_controller import scrape_product
from PIL import Image

st.set_page_config(page_title="Amazon Scraper", layout="wide")
st.title("Amazon/Flipkart Product Scraper")

product_url = st.text_input("Enter Product URL:")

if st.button("Extract Product Details"):
    if product_url:
        with st.spinner("Scraping product details..."):
            product_data = scrape_product(product_url)

        st.subheader("Product Name")
        st.write(product_data["product_name"])

        st.subheader("Description")
        st.write(product_data["description"])

        st.subheader("Product Images")
        if product_data["image_path"]:
            cols = st.columns(len(product_data["image_path"]))
            for i, img_path in enumerate(product_data["image_path"]):
                with cols[i]:
                    st.image(Image.open(img_path), use_column_width=True)

        st.subheader("Product Video")
        if product_data["video_path"]:
            st.video(product_data["video_path"])
        else:
            st.write("No video found.")
    else:
        st.error("Please enter a valid product URL.")

import streamlit as st
import fitz  # PyMuPDF
import json
import re

# Convert PDF to JSON
def convert_pdf_to_json(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    json_data = {"results": []}
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        words = page.get_text("words")  # Extract words as a list
        page_data = {
            "page": page_num,
            "words": [{"text": w[4], "xmin": w[0], "ymin": w[1], "xmax": w[2], "ymax": w[3]} for w in words],
            "raw_text": page.get_text("text")  # Optionally store raw text
        }
        json_data["results"].append({"filename": "daily_report.pdf", "page_data": [page_data]})

    return json_data

# Generate Snow Report Narrative
def generate_snow_report(json_data):
    text_data = json_data['results'][0]['page_data'][0]['raw_text']
    
    # Extract key information
    base_temp_am = re.search(r'Base Temp (\d+)', text_data).group(1)
    summit_temp_am = re.search(r'Summit Temp (\d+)', text_data).group(1)
    base_temp_pm = re.search(r'Base Temp (\d+)', text_data).group(1)
    summit_temp_pm = re.search(r'Summit Temp (\d+)', text_data).group(1)
    closed_trails = re.findall(r'(\w+)\s\(East Peak\)\sClosed', text_data)

    # Create the snow report narrative
    snow_report = f"""
    Today at Windham Mountain, we’re looking at a base temperature starting at {base_temp_am}°F, rising to {base_temp_pm}°F by midday. Summit temps range from {summit_temp_am}°F in the morning to {summit_temp_pm}°F in the afternoon.
    
    Trail Updates:
    Key trails are open with freshly groomed paths. Trails like {', '.join(closed_trails[:3])} are closed for maintenance.
    
    Join us for a great day on the mountain!
    """
    return snow_report

# Streamlit Interface
st.title("Windham Mountain Snow Report Generator")

# Upload PDF file
uploaded_file = st.file_uploader("Upload daily snow report PDF", type="pdf")

if uploaded_file is not None:
    st.write("Processing PDF...")
    json_data = convert_pdf_to_json(uploaded_file)
    snow_report = generate_snow_report(json_data)
    
    # Display snow report
    st.subheader("Generated Snow Report")
    st.text(snow_report)

    # Option to download the report
    st.download_button("Download Report", snow_report, file_name="daily_snow_report.txt")


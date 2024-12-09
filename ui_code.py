import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Function to read the image and encode it as base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Paths to your images
background_image_path = "/Users/guoziqi/CSE583/LeOpardLink/images_design/dot.png"
main_page_image_path = "/Users/guoziqi/CSE583/LeOpardLink/images_design/LOLcroped.png"

# Encode the background image
base64_image = get_base64_image(background_image_path)

# Background CSS
def get_background_css(page):
    if page == "main":
        # CSS for the main page (solid color)
        return """
        <style>
        .stApp {
            background-color: #E1C9AD; /* Light brown */
        }
        </style>
        """
    elif page == "upload":
        # CSS for the upload page (image background)
        return f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{base64_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            color: white; /* Ensure text is readable */
        }}

        .main-content {{
            position: relative;
            z-index: 1;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            max-width: 80%;
            margin: auto;
        }}
        </style>
        """
#botton css
button_css = """
<style>
/* General button style */
div.stButton > button {
    background-color: #4CAF50; /* Green */
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}

/* Hover effect */
div.stButton > button:hover {
    background-color: #45a049; /* Darker green */
    transform: scale(1.05); /* Slightly enlarge the button */
}

/* Button focus effect */
div.stButton > button:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
"""

# Inject the CSS into Streamlit
st.markdown(button_css, unsafe_allow_html=True)

# Set default page in session state
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Apply background CSS based on the current page
st.markdown(get_background_css(st.session_state["page"]), unsafe_allow_html=True)

# Main Page
# Main Page
def main_page():
    # Display the main page image
    st.image(main_page_image_path, width=600)  # Updated parameter

    # Title and input field
    st.title("Welcome to LeOpardLink!")
    name = st.text_input("What's your name:")
    if st.button("Start"):
        if name.strip():
            st.session_state["name"] = name
            st.session_state["page"] = "upload"  # Navigate to upload page
        else:
            st.error("Please enter a valid name.")

# Upload Page
def upload_page():
    st.title(f"Hello, {st.session_state.get('name', 'User')}!")
    st.write("You can now upload your data.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the DataFrame
        st.write("### Uploaded DataFrame")
        st.dataframe(df)

        # Process and generate plot
        try:
            plot = LeOpardLink(df)  # Call your custom function
            st.pyplot(plot)
        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Generate Link Button
        if st.button("Generate Link"):
            try:
                # Replace this with the actual CSS generation logic
                generated_link = generate_css_link(df)  # Placeholder for your function
                st.success("Link generated successfully!")
                st.markdown(f"[Download Link]({generated_link})")  # Display the link
            except Exception as e:
                st.error(f"An error occurred while generating the link: {e}")

    # Back to Main Page button
    if st.button("Back to Main Page"):
        st.session_state["page"] = "main"  # Navigate back to the main page

#Leoparodlink function goes here
#####

def LeOpardLink(df):
    """
    Add LeOpardLink function and generating the plot.
    The function should return a figure (fig) object.
    """



# Render the appropriate page
if st.session_state["page"] == "main":
    main_page()
elif st.session_state["page"] == "upload":
    upload_page()
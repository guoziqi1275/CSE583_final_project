import streamlit as st
import base64
import pandas as pd
#streamlit run /Users/guoziqi/CSE583/LeOpardLink/UI_Design/ui_code/ui_code.py

# Add a title to your app
st.title("Welcome to LeOpardLink!")

# Add a text input field
name = st.text_input("What's your name?")

# Add a button
if st.button("Greet Me"):
    if name:
        st.write(f"Hello, {name}! 🎉")
    else:
        st.write("Hello, Stranger! Please enter your name for a personalized greeting.")


#https://docs.streamlit.io/develop/concepts/design/dataframes

#link creation area
st.title("Create your Link here")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

#Leoparodlink function goes here
#####
def LeOpardLink(df):
    """
    Add LeOpardLink function and generating the plot.
    The function should return a figure (fig) object.
    """

#Process the uploaded CSV
if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write("### Uploaded DataFrame")
    st.dataframe(df)

    # Generate plot using the custom function
    st.write("### Generated Plot")
    try:
        plot = process_and_plot_data(df)  # Call your custom function here
        st.pyplot(plot)  # Display the plot in Streamlit
    except Exception as e:
        st.error(f"An error occurred while generating the plot: {e}")

# Add custom CSS, button...
custom_css = """
<style>
body {
    background-color: #E1C9AD; /* brown */
    color: #E1C9AD; /* Text color */
    font-family: Arial, sans-serif;
}

h1 {
    color: black; /* Welcome to LeOpardLink */
    text-align: center;
}

div.stButton > button {
    background-color: #4CAF50; /* Green button background */
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    font-size: 16px;
    cursor: pointer;
}

div.stButton > button:hover {
    background-color: #45a049; /* Darker green on hover */
}

</style>
"""

# Inject CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

# App content
st.button("Generate plot")




# Add the CSS for the toggle switch
switch_css = """
<style>
/* The switch container */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

/* Slider circle */
.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

/* When checked */
input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}
</style>
"""

# Inject CSS into Streamlit
st.markdown(switch_css, unsafe_allow_html=True)

# Add the toggle switch HTML
st.markdown(
    """
    <label class="switch">
      <input type="checkbox">
      <span class="slider"></span>
    </label>
    """,
    unsafe_allow_html=True
)

# Streamlit interaction
st.write("This is a static toggle switch.")

#background

# Function to read the image and encode it as base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your image
image_path = "/Users/guoziqi/CSE583/LeOpardLink/images_design/dot.png"

# Encode the image as base64
base64_image = get_base64_image(image_path)

# Define the CSS for the background and ensure content is visible
background_css = f"""
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
    z-index: 1; /* Ensure content is above the background */
    padding: 20px; /* Add padding for better spacing */
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background for contrast */
    border-radius: 10px; /* Optional: rounded corners for content box */
    max-width: 80%;
    margin: auto; /* Center the content horizontally */
}}


"""

# Inject the CSS and HTML into the Streamlit app
st.markdown(background_css, unsafe_allow_html=True)
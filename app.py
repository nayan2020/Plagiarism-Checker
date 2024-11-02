import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import StringIO
import pandas as pd
import plotly.express as px
import os
import glob

file_names = None
file_contents = None
directory="files_container" # default file
 


# ********************************************************
#   Function: delete_folder
# 
#   Remove every element from folder
# 
#   Input:
#       folder_path       : input file path
#
#   Output:
#       None
#
# ********************************************************

def delete_folder(
        directory,
        file_type = '*'
        ):
    try:
        files = glob.glob(os.path.join(directory, file_type))
        for file in files:
            os.remove(file)
    except FileNotFoundError:
        st.write(f"Folder '{directory}' not found.")
    except OSError as e:
        st.write(f"Error deleting folder '{directory}': {e}")

# ********************************************************
#   function: save_multiple_files
# 
#   Store the uploded file in local
# 
#   Input:
#       uploaded_files      : multiple files
#       directory           : files stored location              
#
#   Output:
#       None
#
# ********************************************************
def save_multiple_files(
        uploaded_files,
    ):
    
    global directory
    delete_folder(directory)
    os.makedirs(directory, exist_ok=True)
    for uploaded_file in uploaded_files:
        filepath = os.path.join(directory, uploaded_file.name)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()

        with open(filepath, 'w') as f:
            f.write(string_data)

# ********************************************************
#   function: user_input
# 
#   Remove every element from folder
# 
#   Input:
#       None              
#
#   Output:
#       populate Heat Map and line graph
#
# ********************************************************
def calculation_input_and_populate_output():
    global directory
    # *********** Load and read the content of each  file ***********

    extracted_files = os.listdir(directory)
    extracted_files.sort()
    
    global file_contents
    file_contents = {}
    for file_name in extracted_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents[file_name] = f.read()
    

    # Get the list of filenames and their respective content
    global file_names
    file_names = list(file_contents.keys())
    file_texts = list(file_contents.values())

    # ******************* Calculate Part *******************

    # Calculate pairwise cosine similarity on the file contents using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(file_texts)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    # ********************* Populate Part *********************

    
    tab1, tab2 = st.tabs(["Heat Map presentation", "Line presentation"]) # ["Streamlit theme (default)", "Plotly native theme"]
    with tab1:
        # ***************** HeatMap *****************
        fig = px.imshow(similarity_matrix,
                    title="Plagiarism Heatmap",
                    #labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                    x=file_names,
                    y=file_names,
                    text_auto=True,                     # Automatically adds annotations on each cell with its value.
                    color_continuous_scale='Blues',     # (e.g., Viridis, Cividis, Blues).
                    range_color=[0, 1],                 # comment out for auto 
                    aspect='auto',                     #  ('auto', 'equal', 'cube'),

                   )
        
        st.plotly_chart(fig, theme=None, selection_mode=('points', 'box', 'lasso'), use_container_width=True) # plotly_dark, streamlit
    
    with tab2:
        # ***************** Line Chart *****************
        chart_data = pd.DataFrame(data=similarity_matrix, columns=file_names)
        st.line_chart(chart_data,y=file_names)



def main():
    st.set_page_config(page_title="Comparison Checker", page_icon=":bar_chart:", layout="wide")
    st.header("Plagiarism Cheker for Multiple Files")

    global directory
    if st.button("Click here to show the result"):
        if os.listdir(directory):
            calculation_input_and_populate_output()
        else:
            st.write("Folder is Empty, First upload the Data...")

    #   details about sidebar 
    with st.sidebar:
        # show the modified navigation button
        button_position_1, button_position_2 = st.columns([.5, 1])
        with button_position_1:
            st.page_link("app.py",label="Home",  icon="🏠")
        with button_position_2:
            st.page_link("pages/compair_page.py", label="Comparison", icon="🔎")

        # remove the default navigation bar
        st.markdown("""
        <style>
            
            [data-testid="stSidebarNavItems"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)

        # upload the multiple file
        st.title("Upload:")
        multiple_file = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        
        # processing 
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                save_multiple_files(multiple_file)
                st.success("Done")

        # button for clear the folder
        if st.button("Delete Uploaded Data", type="primary"):
            if os.listdir(directory):
                delete_folder(directory)
            else:
                st.write("Folder is Empty")
            



if __name__ == "__main__":
    main()

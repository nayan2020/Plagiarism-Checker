import os
import streamlit as st

file_names = None
file_contents = None

# ********************************************************
#   Function: upload_data
# 
#   Fetch the data from directory
# 
#   Input:
#       None      
#
#   Output:
#       None
#
# ********************************************************
def upload_data():
    extracted_files = os.listdir("files_container")
    
    global file_contents
    file_contents = {}
    for file_name in extracted_files:
        file_path = os.path.join("files_container", file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents[file_name] = f.read()
    

    # Get the list of filenames and their respective content
    global file_names
    file_names = list(file_contents.keys())

# ********************************************************
#   Function: compair_multiple_code
# 
#   Show the compair code side by side
# 
#   Input:
#       None      
#
#   Output:
#       None
#
# ********************************************************
def compair_multiple_code():
    global file_name_1_pre
    global file_name_2_pre
    
    col1, col2 = st.columns(2)

    with col1:
        file_name_1 = st.selectbox(
            "Select the file 1",
            file_names,
            index=None,
            placeholder="Select file 1...",
        )
        if file_name_1:
            file_path = os.path.join("files_container", file_name_1)
            with open(file_path, 'r', encoding='utf-8') as f:
                st.code(f.read())

    with col2:
        file_name_2 = st.selectbox(
            "Select the file 2",
            file_names,
            index=None,
            placeholder="Select file 2...",
        )
        if file_name_2:
            file_path = os.path.join("files_container", file_name_2)
            with open(file_path, 'r', encoding='utf-8') as f:
                st.code(f.read())
    
    css='''
    <style>
        section.main>div {
            padding-bottom: 1rem;
        }
        [data-testid="stCode"] {
            overflow: auto;
            height: 70vh;
        }
        .stMainBlockContainer{
            width: 100%;
            padding: 6rem 1rem 10rem;
            min-width: auto;
            max-width: 100rem;
        }
        
    </style>
    '''
   
    st.markdown(css, unsafe_allow_html=True)
            


def main():
    st.set_page_config(page_title="Comparison Checker", page_icon=":bar_chart:", layout="wide")
    st.header("Comparison between two file")

    if os.listdir("files_container") == []:
        st.write("Folder is Empty, First upload the Data...")
    

    # if os.listdir("files_container"):
    upload_data()
    compair_multiple_code()

    
    st.markdown("""
        <style>
            
            [data-testid="stSidebarNavItems"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)


    with st.sidebar:
        button_position_1, button_position_2 = st.columns(2)
        with button_position_1:
            st.page_link("app.py",label="Home",  icon="🏠")
        with button_position_2:
            st.page_link("pages/compair_page.py", label="Comparison", icon="🔎")

        
    
    



if __name__ == "__main__":
    main()

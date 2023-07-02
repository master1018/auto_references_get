import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from pdf_parse import *
from paper_get import *

def aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    selection_mode = 'multiple' # 定义单选模式，多选为'multiple'
    enable_enterprise_modules = True # 设置企业化模型，可以筛选等
    #gb.configure_default_column(editable=True) #定义允许编辑
    
    return_mode_value = DataReturnMode.FILTERED  #__members__[return_mode]
    gb.configure_selection(selection_mode, use_checkbox=True) # 定义use_checkbox
    
    gb.configure_side_bar()
    gb.configure_grid_options(domLayout='normal')
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    #gb.configure_default_column(editable=True, groupable=True)
    gridOptions = gb.build()
    
    update_mode_value = GridUpdateMode.MODEL_CHANGED
    
    grid_response = AgGrid(
                        df, 
                        gridOptions=gridOptions,
                        fit_columns_on_grid_load = True,
                        data_return_mode=return_mode_value,
                        update_mode=update_mode_value,
                        enable_enterprise_modules=enable_enterprise_modules,
                        theme='streamlit'
                        )  
    #df = grid_response['data']
    selected = grid_response['selected_rows']
    ret_list = []
    if len(selected) == 0:
        return -1
    else:
        for i in range(0, len(selected)):
            ret_list.append(selected[i]['Reference'])  
        return ret_list

def list_to_df(list_t):
    df = pd.DataFrame(np.array(list_t))
    df.columns = ['Reference']
    return df

def init():
    if "upload_file" not in st.session_state:
        st.session_state.upload_file = None
    if "references" not in st.session_state:
        st.session_state.references = None 
    if "bibtex" not in st.session_state:
        st.session_state.bibtex = None
    if "select_references" not in st.session_state:
        st.session_state.select_references = None
    return

def callback():
    if st.session_state.upload_file == None:
        return
    bytes_data = st.session_state.upload_file.getvalue()
    fp = open("./output/input.pdf", "wb")
    fp.write(bytes_data)
    fp.close()
    st.session_state.upload_file = None
    get_references("./output/input.pdf")
    reference_list = []
    fp = open("./output/tmp_output", "r")
    fp.readline()
    while True:
        line = fp.readline()
        if not line:
            break
        if line[len(line) - 1] == "\n":
            line = line[0: len(line) - 1]
        reference_list.append(line)
    st.session_state.references = reference_list

def callback2():
    st.session_state.bibtex = None
    st.session_state.bibtex = []
    if st.session_state.select_references == -1:
        return
    for i in range(0, len(st.session_state.select_references)):
        q = st.session_state.select_references[i]
        print(q)
        try:
            bib = down_reference(q)
            st.session_state.bibtex.append(bib)
        except:
            count = 0
            while count < 3:
                try:
                    bib = down_reference(q)
                    break
                except:
                    count += 1
                    print("[-] falied " + str(count))
                    continue
            if count == 3:
                st.session_state.bibtex.append("Download failed: " + st.session_state.select_references[i])
            else:
                st.session_state.bibtex.append(bib)
def main():
    init()
    st.text("Upload the paper...")
    st.session_state.upload_file = st.file_uploader(label="", type="pdf")
    st.button(label="进行解析", on_click=callback)
    if st.session_state.references != None:
        st.session_state.select_references = aggrid(list_to_df(st.session_state.references))
        st.button(label="Download Reference", on_click=callback2)
        if st.session_state.bibtex != None:
            for i in range(0, len(st.session_state.select_references)):
                with st.expander(st.session_state.select_references[i]):
                    st.code(st.session_state.bibtex[i])

if __name__ == "__main__":
    st.set_page_config(
        "论文文献自动下载器",
        "📊",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()
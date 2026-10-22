import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the deatil of New Subject")
    sub_id=st.text_input("Suject Code",placeholder="BMC201")
    sub_name=st.text_input("Subject Name",placeholder="Communiation")
    sub_section=st.text_input("Section",placeholder="Batch A")

    if st.button("Create Subject Now",type="primary",width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject Created Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"ERROR:{e}")
        else:
            st.warning("Please Fill all the field")            
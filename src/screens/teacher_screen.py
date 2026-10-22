import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exist,teacher_login,create_teacher,get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    #teacher_screen_login()
    if "teacher_data" in st.session_state:
          teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
         teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
         teacher_screen_register()


def teacher_dashboard():
      teacher_data=st.session_state.teacher_data
      col1,col2=st.columns(2,vertical_alignment="center",gap="large")
      with col1:
            header_dashboard()      
      with col2:
            st.subheader(f""""Welcome {teacher_data["name"]}""")
            if st.button("Logout",type="secondary",shortcut="control+backspace"):
               st.session_state["is_logged_in"]=False
               del st.session_state.teacher_data
               st.rerun()
      st.space()
      if "current_teacher_tab" not in st.session_state:
            st.session_state.current_teacher_tab="take_attendence"
      tab1,tab2,tab3=st.columns(3)         

      with tab1:
            type1="primary" if st.session_state.current_teacher_tab=="take_attendence" else "tertiary"
            if st.button("Take Attendence",type=type1,width="stretch",icon=":material/ar_on_you:"):
                  st.session_state.current_teacher_tab="take_attendence"
                  st.rerun()
      with tab2:
            type2="primary" if st.session_state.current_teacher_tab=="manage_subjects" else "tertiary"
            if st.button("Manage Subjects",type=type2,width="stretch",icon=":material/book_ribbon:"):
                  st.session_state.current_teacher_tab="manage_subjects"
                  st.rerun()
      with tab3:
            type3="primary" if st.session_state.current_teacher_tab=="attendence_records" else "tertiary"
            if st.button("Attendence Records",type=type2,width="stretch",icon=":material/cards_stack:"):
                  st.session_state.current_teacher_tab="attendence_records"
                  st.rerun()        

      if st.session_state.current_teacher_tab == "take_attendence":
        teacher_tab_take_attendence()

      if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

      if st.session_state.current_teacher_tab == "attendence_records":
        teacher_tab_attendence_records()            

st.divider()

def teacher_tab_take_attendence():
      st.header("Take Ai Attendence")
def teacher_tab_manage_subjects():
      teacher_id=st.session_state.teacher_data["teacher_id"]
      col1,col2=st.columns(2)
      with col1:
          st.header("Manage Subjects")
      with col2:
            if st.button("Create New Subject",width="stretch"):
                  create_subject_dialog(teacher_id)   
      #List all Subject
      subjects=get_teacher_subjects(teacher_id)
      if subjects:
            for sub in subjects:
                  stats=[
                        ("🫂","Students",sub["total_students"])
                        ("🕛","Classes",sub["total_classes"])
                  ]
            def share_btn():
                  if st.button(f"Share Code {sub["name"]}",key=f"share_{sub["subject_code"]}",icon=":material/share:"):
                       # share_subject_dialog(sub["name"],sub["subject_code"])
                        st.space()

            subject_card(
                  name=sub["name"],
                  code=sub["subject_code"],
                  section=sub["section"],
                  stats=stats,
                  footer_callback=share_btn
            ) 
      else:
            st.info("No Subject Found")                 


def teacher_tab_attendence_records():
      st.header("Take Attendece records")

def login_teacher(username,password):
      if not username or not password:
            return False
      teacher=teacher_login(username,password) 

      if teacher:
            st.session_state.user_role="teacher"
            st.session_state.teacher_data=teacher
            st.session_state.is_logged_in=True
            return True 

      return False        

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_conf_pass):
      if not teacher_username or not teacher_name or not teacher_pass:
            return False,  "All fields are required"
      if check_teacher_exist(teacher_username):
            return False ,"username Already exist"
      if teacher_pass != teacher_conf_pass:
            return False ,"Passswrod dose't match"
      try:
            create_teacher(teacher_username,teacher_pass,teacher_name)
            return True,"Succesfully created Login now"
      except Exception as e:
            return False, f"Unexpected error  :{e}"                  
   

def teacher_screen_login():
         col1,col2=st.columns(2,vertical_alignment="center",gap="large")
         with col1:
            header_dashboard()      
         with col2:
            if st.button("Go Back To Home",type="secondary",shortcut="control+backspace"):
                    st.session_state["login_type"]=None
                    st.rerun()
            #st.header("Teacher Screen")
         st.header("Login Using Password",text_alignment="center")
         st.space() 
         st.space()

         teacher_usesrname=st.text_input("Enter Username",placeholder="rohit123")
         teacher_pass=st.text_input("enter the password",type="password",placeholder="enter password")
         st.divider()

         btn1,btn2=st.columns(2)
         with btn1:
              if st.button("Login",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
                    if login_teacher(teacher_usesrname,teacher_pass):
                          st.toast("welcome back",icon='👋')
                          import time
                          time.sleep(1)
                          st.rerun() 
                    else:
                          st.error("invalid username or password")      

         with btn2:
              if st.button("Register Instead",type="primary",key="loginbackbtn",icon=":material/passkey:",width="stretch"):
                   st.session_state.teacher_login_type="register"     


def teacher_screen_register():
        col1,col2=st.columns(2,vertical_alignment="center",gap="xxlarge")
        with col1:
             header_dashboard()
        with col2:
             if st.button("Go Back To Home",type="secondary",shortcut="control+backspace"):
                         st.session_state["login_type"]=None
                         st.rerun()
                  
        st.header("Teacher Screen")
        st.header("Register Your techer Profile")
        st.space() 
        teacher_username=st.text_input("Enter Username",placeholder="@rohit123")
        teacher_name=st.text_input("Enter Teacher name",placeholder="Arun")
        teacher_pass=st.text_input("enter the password",type="password")
        teacher_conf_pass=st.text_input("confirm password",type="password")
        st.divider()

        btn1,btn2=st.columns(2)
        with btn1:
              if st.button("Register now",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
                         success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_conf_pass)
                         if success:
                               st.success(message)
                               import time
                               time.sleep(2)
                               st.session_state.teacher_login_type="login"
                               st.rerun()
                         else:
                               st.error(message)      
        with btn2:
              if st.button("Login",type="primary",icon=":material/passkey:",width="stretch"):
                   st.session_state.teacher_login_type="login"     
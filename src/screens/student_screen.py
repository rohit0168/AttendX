import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.database.db import check_teacher_exist,teacher_login,create_teacher
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendence
from src.database.db import get_all_students,create_student
import time
from src.pipelines.face_pipeline import get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding 
def student_dashboard():
      st.header("Dash board Here")
def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
          student_dashboard()
          return
    col1,col2=st.columns(2,vertical_alignment="center",gap="large")
    with col1:
            header_dashboard()      
    with col2:
            if st.button("Go Back To Home",type="secondary",shortcut="control+backspace"):
                st.session_state["login_type"]=None
                st.rerun()
    st.space() 
    st.header("Login Using Face id",text_alignment="center")
    st.space()
    show_registration=False
    photo_source=st.camera_input("Position your face in the center")
    if photo_source:
          img=np.array(Image.open(photo_source))

          with st.spinner("AI is scanning...."):
                detected,all_ids,num_faces=predict_attendence(img)

                if num_faces ==0:
                      st.warning("Faces not Found")
                elif num_faces >1:
                      st.warning("Multple Faces Found")
                else:
                      if detected:
                           student_id=list(detected.keys())[0]
                           all_students=get_all_students()
                           student=next((s for s in  all_students if s["student_id"]==student_id),None)

                           if student:
                                 st.session_state.is_logged_in=True
                                 st.session_state.user_role='student'
                                 st.session_state.student_data=student
                                 st.toast(f"welcome back {student["name"]}")
                                 time.sleep(1)
                                 st.rerun()
                      else:
                            st.info("Face not recognized you might be a new student")
                            show_registration=True
    if show_registration:
          with st.container(border=True):
                st.header("register New Profile")
                new_name=st.text_input("Enter your name",placeholder="E.g Rohit")

                st.subheader("Option 1: Voice Enrollment")
                st.info("Enroll for voice only attendence")

                audio=None
                try:
                      audio_data=st.audio_input("Record a short phase Like I am Present My name is Rohit")
                except:
                      st.error("Auidio Data Failed")
                if st.button("Create Account",type="primary"):
                      if new_name:
                            with st.spinner("Creating Profile"):
                                  img=np.array(Image.open(photo_source))
                                  encodings=get_face_embeddings(img)
                                  if encodings:
                                        face_emb=encodings[0].tolist()

                                        voice_emb=None
                                        if audio_data:
                                              voice_emb=get_voice_embedding(audio_data.read())

                                        response_data=create_student(new_name,face_emb,voice_emb)

                                        if response_data:
                                              train_classifier()
                                              st.session_state.is_logged_in=True
                                              st.session_state.user_role='student'
                                              st.session_state.student_data=response_data[0]
                                              st.toast(f"Profile Created  HI {new_name}")
                                              time.sleep(1)
                                              st.rerun()
                                        else:
                                              st.error("Could not Capture your Facial Features for registration")      


                      else:
                            st.warning("Please enter your name")
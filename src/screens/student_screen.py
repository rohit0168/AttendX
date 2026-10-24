import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.database.db import check_teacher_exist,teacher_login,create_teacher
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendence
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject 
import time
from src.pipelines.face_pipeline import get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding 
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
def student_dashboard():
      st.header("Dash board Here")
      student_data=st.session_state.student_data
      student_id=student_data["student_id"]
      col1,col2=st.columns(2,vertical_alignment="center",gap="large")
      with col1:
            header_dashboard()      
      with col2:
            st.subheader(f""""Welcome {student_data["name"]}""")
            if st.button("Logout",type="secondary",shortcut="control+backspace"):
               st.session_state["is_logged_in"]=False
               del st.session_state.student_data
               st.rerun()  

      st.space()


      col1,col2=st.columns(2)
      with col1:
            st.header("Your enrolled subjects")
      with col2:
           if st.button("Enroll in subject",type="primary",width="stretch"):
                 enroll_dialog()  

      st.divider()

      with st.spinner("Loading Your Enrolled Subjects"):
            subjects=get_student_subjects(student_id)
            logs=get_student_attendance(student_id) 
      stats_map={}
      for log in logs:
            sid=log["subject_id"]

            if sid not in stats_map:
                  stats_map[sid]={"total":0,"attended":0}

            stats_map[sid]["total"]+=1
            if logs.get("is_present"):
                  stats_map[sid]["attende"]+=1
      cols=st.columns(2)
      for i,sub_node in enumerate(subjects):
            sub=sub_node["subjects"]
            sid=sub["subject_id"]

            stats=stats_map.get(sid,{"total":0,"attended":0})
            def unenroll_button():
                  if st.button("Unenroll from the course",type="tertiary",width="stretch",icon=":material/delete_forever:"):
                        unenroll_student_to_subject(student_id,sid)    
                        st.toast(f"Unenrolled from {sub["name"]} Sucessfully")
                        st.rerun()
            with cols[i%2]:
                  subject_card(
                       name=sub["name"],
                       code=sub["subject_code"],
                       section=sub["section"],
                       stats=[
                            ("📅","Total",stats["total"]),
                            ("☑️","Attended",stats["attended"])
                       ],
                       footer_callback=unenroll_button
                  )

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
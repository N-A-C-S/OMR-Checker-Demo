from omr_main import result
import cv2
import streamlit  as st
import PIL.Image
import numpy as np
import re
from PIL import Image

#correct_answer = ["a","b","b","c","a","b","a","b","a","c","b","c","a","b","d","d","d","a","b","c"]

#st.markdown('<style>body{background-color:coral;}</style>',unsafe_allow_html=True)

st.markdown('<center><h1>OMR Checker APP 🙂<h1></center>',unsafe_allow_html=True)

ch = st.selectbox(
    "Choice",
    [
        "Home",
        "OMR CHECKER",
    ],
    key="main_select",
    )

if ch == "Home":
    st.markdown('<center><h3>HOME<h3></center>',unsafe_allow_html=True)

    a = '<p style="text-align: justify;font-size:20px;">OMR Checker APP is an APP that will help the teachers get the results of'
    a+='answer sheet of the students. This will help the teacher to grade the students faster and provide faster results.'
    a+=' </p><br>'
    st.markdown(a,unsafe_allow_html=True)

    st.markdown('<center><h3>FEATURES<h3></center>',unsafe_allow_html=True)
    a = "<p style='text-align: justify;font-size:20px;'><ul><li style='text-align: justify;font-size:20px;'>Interactive Dashboard to Generate OMR Scores Easily</li>"
    a+="<li style='text-align: justify;font-size:20px;'>The images should be in jpeg,png or jpeg format</li>"
    a+="<li style='text-align: justify;font-size:20px;'>The OMR Layout is restricted to the Sample displayed</li><br>"
    st.markdown(a,unsafe_allow_html=True)

    
    st.markdown('<center><h3>SAMPLE IMAGES<h3></center>',unsafe_allow_html=True)
    image = Image.open('sam2.jpeg')
    st.image(image, use_column_width=True)

elif ch == "OMR CHECKER":
    st.markdown('<center><h3>OMR-CHECKER<h3></center>',unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload an OMR Sheet", type = ["png","jpeg","jpg"])

    collect_answers = lambda x : [str(i) for i in  re.split("[^a-z]",x) if i != ""]
    fixed_ans = st.multiselect("Please Select corrext Answers in order ",['a','b','c','d']*30) 
    if uploaded_image is not None:
        image = PIL.Image.open(uploaded_image).convert("RGB")
        img_array = np.array(image)
        enrollment_no,test_id,answer_list = result(img_array)
        
        st.info("Enrollment Number : "+enrollment_no)
        st.info("Test ID           : "+str(test_id))
        if(len(fixed_ans)!=30):
            st.write("Choose the Correct number of Options !!")
        else:
            right = 0
            wrong = 0
            unattempted = 0
            for i in range(30):
                if(fixed_ans[i]==answer_list[i]):
                    right +=1
                elif(answer_list[i]=='x'):
                    unattempted+=1
                else:
                    wrong+=1
            st.success("Correctly Marked  : "+str(right))
            st.error("Wrongly Marked  : "+str(wrong))
            st.warning("Not Marked  : "+str(unattempted))
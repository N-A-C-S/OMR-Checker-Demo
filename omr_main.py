import cv2
import numpy as np
import util
import imutils
from PIL import Image

def result(img):
    width = 700
    height = 700
    img = cv2.resize(img,(width,height))
    img_cont = img.copy()
    img_cp = img.copy()
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray,(5,5),1)
    img_edge = cv2.Canny(img_blur,1,30)

    contours , hierarchy = cv2.findContours(img_edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img_cont,contours,-1,(0,255,0),5)

    r = util.rectContour(contours)

    details = util.getCornerPoints(r[0])
    answers2 = util.getCornerPoints(r[1])
    answers1 = util.getCornerPoints(r[2])

    cv2.drawContours(img_cp,answers2,-1,(255,0,0),5)
    cv2.drawContours(img_cp,answers1,-1,(0,255,0),5)
    cv2.drawContours(img_cp,details,-1,(0,0,255),5)

    details = util.reorder(details)
    answers2 = util.reorder(answers2)
    answers1 = util.reorder(answers1)

    #bird eye view of details
    pts1 = np.float32(details)
    pts2 = np.float32([[0, 0],[width, 0], [0, height],[width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
    imgWarpColored_details = cv2.warpPerspective(img, matrix, (width, height))
    details_bev = cv2.cvtColor(imgWarpColored_details,cv2.COLOR_BGR2GRAY)


    pts1_ans1 = np.float32(answers1)
    pts2_ans1 = np.float32([[0, 0],[width, 0], [0, height],[width, height]])
    matrix = cv2.getPerspectiveTransform(pts1_ans1, pts2_ans1) # GET TRANSFORMATION MATRIX
    imgWarpColored_ans1 = cv2.warpPerspective(img, matrix, (width, height))
    ans1_bev = cv2.cvtColor(imgWarpColored_ans1,cv2.COLOR_BGR2GRAY)

    #bird eye view of answers2
    pts1_ans2 = np.float32(answers2)
    pts2_ans2 = np.float32([[0, 0],[1000, 0], [0, 700],[1000, 700]])
    matrix = cv2.getPerspectiveTransform(pts1_ans2, pts2_ans2) # GET TRANSFORMATION MATRIX
    imgWarpColored_ans2 = cv2.warpPerspective(img, matrix, (1000, 700))
    ans2_bev = cv2.cvtColor(imgWarpColored_ans2,cv2.COLOR_BGR2GRAY)

    enrollment_no = details_bev[170:700, 30:420]
    test_id = details_bev[170:680,480:680]

    answers_1t5 = ans1_bev[180:680,60:280]
    answers_6t10 = ans1_bev[180:680,415:635]

    answers_11t12 = ans2_bev[200:640,30:150]
    answers_13t14 = ans2_bev[200:640,240:360]
    answers_15t16 = ans2_bev[200:640,435:575]
    answers_17t18 = ans2_bev[200:640,640:760]
    answers_19t20 = ans2_bev[200:640,840:960]

    enrol_thresh = cv2.threshold(enrollment_no,150,255,cv2.THRESH_BINARY_INV)[1]
    box_enroll = util.splitBoxes(enrol_thresh,10,10)

    tid_thresh = cv2.threshold(test_id,150,255,cv2.THRESH_BINARY_INV)[1]
    box_tid = util.splitBoxes(tid_thresh,10,5)

    ans1_thresh = cv2.threshold(answers_1t5,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a1 = util.splitBoxes(ans1_thresh,5,4)

    ans2_thresh = cv2.threshold(answers_6t10,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a2 = util.splitBoxes(ans2_thresh,5,4)

    ans3_thresh = cv2.threshold(answers_11t12,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a3 = util.splitBoxes(ans3_thresh,5,4)

    ans4_thresh = cv2.threshold(answers_13t14,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a4 = util.splitBoxes(ans4_thresh,5,4)

    ans5_thresh = cv2.threshold(answers_15t16,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a5 = util.splitBoxes(ans5_thresh,5,4)

    ans6_thresh = cv2.threshold(answers_17t18,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a6 = util.splitBoxes(ans6_thresh,5,4)

    ans7_thresh = cv2.threshold(answers_19t20,150,255,cv2.THRESH_BINARY_INV)[1]
    box_a7 = util.splitBoxes(ans7_thresh,5,4)

    arr_enroll = util.getArray(10,10,box_enroll)
    ENROLLMENT_NO = " "
    for i in range(10):
        ENROLLMENT_NO  = ENROLLMENT_NO + str((np.argmax(arr_enroll.T[i])+1)%10)
    
    arr_tid = util.getArray(10,5,box_tid)
    TEST_ID=""
    for i in range(5):
        TEST_ID += str((np.argmax(arr_tid.T[i])+1)%10)
    
    options = ["a","b","c","d"]
    ANSWER = []
    arr_1t5 = util.getArray(5,4,box_a1)
    arr_6t10 = util.getArray(5,4,box_a2)
    for i in range(5):
        if(np.max(arr_1t5[i])!=0):
            ANSWER.append(options[np.argmax(arr_1t5[i])])
        else:
            ANSWER.append(" ")
    for i in range(5):
        if(np.max(arr_6t10[i])!=0):
            ANSWER.append(options[np.argmax(arr_6t10[i])])
        else:
            ANSWER.append(" ")
    
    arr_11t12 = util.getArray(5,4,box_a3)
    arr_13t14 = util.getArray(5,4,box_a4)
    arr_15t16 = util.getArray(5,4,box_a5)
    arr_17t18 = util.getArray(5,4,box_a6)
    arr_19t20 = util.getArray(5,4,box_a7)

    i1=0
    i2=3

    ####11-12
    if(np.max(arr_11t12[i1])!=0):
        ANSWER.append(options[np.argmax(arr_11t12[i1])])
    else:
        ANSWER.append(" ")

    if(np.max(arr_11t12[i2])!=0):
        ANSWER.append(options[np.argmax(arr_11t12[i2])])
    else:
        ANSWER.append(" ")

    ####13-14
    if(np.max(arr_13t14[i1])!=0):
        ANSWER.append(options[np.argmax(arr_13t14[i1])])
    else:
        ANSWER.append(" ")

    if(np.max(arr_13t14[i2])!=0):
        ANSWER.append(options[np.argmax(arr_13t14[i2])])
    else:
        ANSWER.append(" ")

    ####15-16
    if(np.max(arr_15t16[i1])!=0):
        ANSWER.append(options[np.argmax(arr_15t16[i1])])
    else:
        ANSWER.append(" ")

    if(np.max(arr_15t16[i2])!=0):
        ANSWER.append(options[np.argmax(arr_15t16[i2])])
    else:
        ANSWER.append(" ")

    ####17-18
    if(np.max(arr_17t18[i1])!=0):
        ANSWER.append(options[np.argmax(arr_17t18[i1])])
    else:
        ANSWER.append(" ")

    if(np.max(arr_17t18[i2])!=0):
        ANSWER.append(options[np.argmax(arr_17t18[i2])])
    else:
        ANSWER.append(" ")

    ####19-20
    if(np.max(arr_19t20[i1])!=0):
        ANSWER.append(options[np.argmax(arr_19t20[i1])])
    else:
        ANSWER.append(" ")

    if(np.max(arr_19t20[i2])!=0):
        ANSWER.append(options[np.argmax(arr_19t20[i2])])
    else:
        ANSWER.append(" ")

    return ENROLLMENT_NO,TEST_ID,ANSWER    

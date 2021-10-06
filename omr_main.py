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

    rlist = []
    #drawing rectangular contours on img_cp
    for i in range(len(r)):
        rc = util.getCornerPoints(r[i])
        cv2.drawContours(img_cp,r[i],-1,(255,0,0),5)
        rc = util.reorder(rc)
        rlist.append(rc)    
    
    #11-14
    pts_1 = np.float32(rlist[0])
    pts_2 = np.float32([[0, 0],[width, 0], [0, height],[width, height]])
    matrix = cv2.getPerspectiveTransform(pts_1, pts_2) # GET TRANSFORMATION MATRIX
    imgWarpColored_details = cv2.warpPerspective(img, matrix, (width, 1000))
    r0 = cv2.cvtColor(imgWarpColored_details,cv2.COLOR_BGR2GRAY)
    r01 = r0[124:700,29:121]
    r01_thresh = cv2.threshold(r01,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r01 = util.splitBoxes(r01_thresh,4,4)
    ans11_14 = util.getArray(4,4,box_r01)

    #15-18
    r02 = r0[124:700,171:263]
    r02_thresh = cv2.threshold(r02,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r02 = util.splitBoxes(r02_thresh,4,4)
    ans15_18 = util.getArray(4,4,box_r02)

    #19-22
    r03 = r0[124:700,313:405]
    r03_thresh = cv2.threshold(r03,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r03 = util.splitBoxes(r03_thresh,4,4)
    ans19_22 = util.getArray(4,4,box_r03)

    #23-26
    r04 = r0[124:700,455:547]
    r04_thresh = cv2.threshold(r04,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r04 = util.splitBoxes(r04_thresh,4,4)
    ans23_26 = util.getArray(4,4,box_r04)

    #27-30
    r05 = r0[124:700,597:689]
    r05_thresh = cv2.threshold(r05,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r05 = util.splitBoxes(r05_thresh,4,4)
    ans27_30 = util.getArray(4,4,box_r05)

    #information
    pts_11 = np.float32(rlist[1])
    pts_21 = np.float32([[0, 0],[width, 0], [0, height],[width, height]])
    matrix = cv2.getPerspectiveTransform(pts_11, pts_21) # GET TRANSFORMATION MATRIX
    imgWarpColored_details1 = cv2.warpPerspective(img, matrix, (width, 1000))
    r1 = cv2.cvtColor(imgWarpColored_details1,cv2.COLOR_BGR2GRAY)

    #enrollment_no
    r11 = r1[140:680,50:400]
    r11_thresh = cv2.threshold(r11,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r11 = util.splitBoxes(r11_thresh,10,10)
    enrollment_no = np.array(util.getArray(10,10,box_r11))
    en = enrollment_no.T
    enl = []
    for i in range(10):
        enl.append(str((np.argmax(en[i])+1)%10))
        eno = "".join(enl)

    #test_id
    r12 = r1[140:680,500:690]
    r12_thresh = cv2.threshold(r12,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r12 = util.splitBoxes(r12_thresh,10,5)
    test_id = np.array(util.getArray(10,5,box_r12))
    tid = test_id.T
    til = []
    for i in range(5):
        til.append(str((np.argmax(tid[i])+1)%10))
    tids = "".join(til)


    pts_13 = np.float32(rlist[2])
    pts_23 = np.float32([[0, 0],[width, 0], [0, height],[width, height]])
    matrix = cv2.getPerspectiveTransform(pts_13, pts_23) # GET TRANSFORMATION MATRIX
    imgWarpColored_details2 = cv2.warpPerspective(img, matrix, (width, 1000))
    r2 = cv2.cvtColor(imgWarpColored_details2,cv2.COLOR_BGR2GRAY)

    #1-5
    r21 = r2[190:690,120:320]
    r21_thresh = cv2.threshold(r21,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r21 = util.splitBoxes(r21_thresh,5,4)
    ans1_5 = util.getArray(5,4,box_r21)
    #print(ans1_5)

    #6-10
    r22 = r2[190:690,420:620]
    r22_thresh = cv2.threshold(r22,100,255,cv2.THRESH_BINARY_INV)[1]
    box_r22 = util.splitBoxes(r22_thresh,5,4)
    ans6_10 = util.getArray(5,4,box_r22)
    #tmp = np.array(ans6_10)
    #for i in range(5):
    #    print(np.argmax(tmp[i]))
    #print(ans6_10)

    a1 = np.array(ans1_5)
    a2 = np.array(ans6_10)
    a3 = np.array(ans11_14)
    a4 = np.array(ans15_18)
    a5 = np.array(ans19_22)
    a6 = np.array(ans23_26)
    a7 = np.array(ans27_30)

    options = ['a','b','c','d']
    answers = []
    for i in range(5):
        if( np.max(a1[i])!=0):
            answers.append(options[np.argmax(a1[i])])
        else:
            answers.append('x')
    for i in range(5):
        if( np.max(a2[i])!=0):
            answers.append(options[np.argmax(a2[i])])
        else:
            answers.append('x')

    for i in range(4):
        if( np.max(a3[i])!=0):
            answers.append(options[np.argmax(a3[i])])
        else:
            answers.append('x')


    for i in range(4):
        if( np.max(a4[i])!=0):
            answers.append(options[np.argmax(a4[i])])
        else:
            answers.append('x')


    for i in range(4):
        if( np.max(a5[i])!=0):
            answers.append(options[np.argmax(a5[i])])
        else:
            answers.append('x')

    for i in range(4):
        if( np.max(a6[i])!=0):
            answers.append(options[np.argmax(a6[i])])
        else:
            answers.append('x')

    for i in range(4):
        if( np.max(a7[i])!=0):
            answers.append(options[np.argmax(a7[i])])
        else:
            answers.append('x')
    return eno,tids,answers
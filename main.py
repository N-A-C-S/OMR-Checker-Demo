from omr_main import result
import cv2

image = cv2.imread("data/test3.jpeg")

enrollment_no,test_id,answer_list = result(image)

print(enrollment_no)
print(test_id)
print(answer_list)
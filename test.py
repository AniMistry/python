import cv2

img = cv2.imread("./img/call.png")

start = (100, 200)
stop = (100, 200)
color = (10, 225, 225)
thickness = 10

res_img = cv2.rectangle(img, start, stop, color, thickness)
cv2.imwrite("./img/call2.png", res_img)
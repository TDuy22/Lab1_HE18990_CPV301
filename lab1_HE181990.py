#Note
#Bấm t để thực hiện function 1
#Bấm r để thực hiện function 2
#Lăn chuột để thực hiện funciton 3
#Các thông số tương tác qua terminal

import cv2
import numpy as np

drawing = False
ix, iy = -1, -1 
rectangle_pts = [] 

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rectangle_pts, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        rectangle_pts = [(x, y)] 
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        img_copy = img.copy()
        drawing = False
        rectangle_pts.append((x, rectangle_pts[0][1]))
        rectangle_pts.append((x, y))
        rectangle_pts.append((rectangle_pts[0][0], y))
        for i in range(4):
            pt1 = rectangle_pts[i]
            pt2 = rectangle_pts[(i + 1) % 4]

            cv2.line(img, pt1, pt2, (0, 255, 0), 2)
        cv2.imshow('image', img_copy)
    
    elif event == cv2.EVENT_MOUSEWHEEL:
        scale = 0.1
        if flags > 0:
            img = create_white_background(640, 480)
            rotation_matrix = cv2.getRotationMatrix2D((x, y), 0, 1+scale)
            rectangle_pts_homogeneous = np.hstack([rectangle_pts, np.ones((4, 1))])

            rectangle_pts = np.dot(rectangle_pts_homogeneous, rotation_matrix.T)

            for i in range(4):
                pt1 = tuple(map(int, rectangle_pts[i]))
                pt2 = tuple(map(int, rectangle_pts[(i + 1) % 4]))
                cv2.line(img, pt1, pt2, (0, 255, 0), 2)
            cv2.imshow('image', img)
        else:
            img = create_white_background(640, 480)
            rotation_matrix = cv2.getRotationMatrix2D((x, y), 0,1- scale)
            rectangle_pts_homogeneous = np.hstack([rectangle_pts, np.ones((4, 1))])

            rectangle_pts = np.dot(rectangle_pts_homogeneous, rotation_matrix.T)

            for i in range(4):
                pt1 = tuple(map(int, rectangle_pts[i]))
                pt2 = tuple(map(int, rectangle_pts[(i + 1) % 4])) 
                cv2.line(img, pt1, pt2, (0, 255, 0), 2)
            cv2.imshow('image', img)  

def create_white_background(width, height):
    return np.ones((height, width, 3), dtype=np.uint8) * 255

def translate_point(x, y, tx, ty):
    translation_matrix = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

    point = np.array([x, y, 1])
    new_point = np.dot(translation_matrix, point)
    return (new_point[0], new_point[1])

def translate_rectangle(tx, ty):
    global rectangle_pts
    img = create_white_background(640, 480)
    for i in range(len(rectangle_pts)):
        rectangle_pts[i] = translate_point(rectangle_pts[i][0], rectangle_pts[i][1], tx, ty)
    for i in range(4):
        pt1 = tuple(map(int, rectangle_pts[i]))
        pt2 = tuple(map(int, rectangle_pts[(i + 1) % 4]))

        cv2.line(img, pt1, pt2, (0, 255, 0), 2)
    return img

def rotate_rectangle(angle_deg):
    global rectangle_pts
    img = create_white_background(640, 480)

    cx, cy = np.mean(rectangle_pts, axis=0)

    rotation_matrix = cv2.getRotationMatrix2D((cx, cy), angle_deg, 1.0)
    rectangle_pts_homogeneous = np.hstack([rectangle_pts, np.ones((4, 1))])

    rectangle_pts = np.dot(rectangle_pts_homogeneous, rotation_matrix.T)

    for i in range(4):
        pt1 = tuple(map(int, rectangle_pts[i]))
        pt2 = tuple(map(int, rectangle_pts[(i + 1) % 4])) 
        cv2.line(img, pt1, pt2, (0, 255, 0), 2)
    return img

if __name__ == "__main__":
    img = create_white_background(640, 480)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)

    while True:
        cv2.imshow('image', img)
        key = cv2.waitKey(1) & 0xFF

        # Press 't' for translation, 'r' for rotation
        if key == ord('t'):
            tx = int(input("Enter translation value for x: "))
            ty = int(input("Enter translation value for y: "))
            img = translate_rectangle(tx, ty)
        elif key == ord('r'):
            angle = float(input("Enter rotation angle: "))
            img = rotate_rectangle(angle)
        elif key == 27:
            break
        elif cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
from fastapi import APIRouter, HTTPException, Response, status
import cv2

router = APIRouter(tags=["Camera Module"])

@router.get("/take-picture")
def take_picture():
    cam = cv2.VideoCapture(2)

    while True:
        ret, image = cam.read()
        cv2.imshow('Image Test',image)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite('/home/ashley/projects/project-samples/images/testimage.jpg', image)
            break

    cam.release()
    cv2.destroyAllWindows()
    return {"data": "picture taken"}

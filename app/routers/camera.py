from fastapi import APIRouter, HTTPException, Response, status
import cv2

router = APIRouter(tags=["Camera Module"])

@router.get("/take-picture")
def take_picture():
    cam = cv2.VideoCapture(2)

    while True:
        result, image = cam.read()
        if result:
            cv2.imshow("Three Tier Security", image)

            # saving image in local storage
            cv2.imwrite('/home/ashley/projects/project-samples/images/testimage.jpg', image)

            # If keyboard interrupt occurs, destroy image
            # window
            cv2.waitKey(0)
            cam.release()
            cv2.destroyWindow("Three Tier Security")
    
        # If captured image is corrupted, moving to else part
        else:
            print("No image detected. Please! try again")
            return {"detail": "Error: No image detected. Please! try again"}
        
        return {"data": "picture taken"}


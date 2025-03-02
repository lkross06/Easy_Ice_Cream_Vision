from __future__ import division
import os
import cv2
import dlib

class EyeTracker:
    def __init__(self):
        #will help predict where face is in image frame
        self._face_detector = dlib.get_frontal_face_detector()

        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        #will help predict where eyes are on face
        self._face_predictor = dlib.shape_predictor(model_path) 

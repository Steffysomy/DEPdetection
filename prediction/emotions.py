import cv2
import numpy as np
import dlib
from imutils import face_utils
import face_recognition
from keras.models import load_model
from statistics import mode
from prediction.utils.datasets import get_labels
from prediction.utils.inference import detect_faces
from prediction.utils.inference import draw_text
from prediction.utils.inference import draw_bounding_box
from prediction.utils.inference import apply_offsets
from prediction.utils.inference import load_detection_model
from prediction.utils.preprocessor import preprocess_input

def main(vid):
    USE_WEBCAM = False # If false, loads video file source

    # parameters for loading data and images
    emotion_model_path = 'D:\\pro final\\prediction\\models\\emotion_model.hdf5'
    emotion_labels = get_labels('fer2013')

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # loading models
    detector = dlib.get_frontal_face_detector()
    emotion_classifier = load_model(emotion_model_path)

    # predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]

    # starting lists for calculating modes
    emotion_window = []

    # starting video streaming

    cv2.namedWindow('window_frame')
    video_capture = cv2.VideoCapture(0)

    # Select video or webcam feed
    cap = None
    if (USE_WEBCAM == True):

        cap = cv2.VideoCapture(0) # Webcam source
    else:
        cap = cv2.VideoCapture(vid) # Video file source
    angry = 0
    sad = 0
    happy = 0
    surprise = 0
    disgust = 0
    fear = 0
    neutral = 0

    while cap.isOpened(): # True:
        ret, bgr_image = cap.read()

        # bgr_image = video_capture.read()[1]

        try:
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        

            faces = detector(rgb_image)

            for face_coordinates in faces:

                x1, x2, y1, y2 = apply_offsets(face_utils.rect_to_bb(face_coordinates), emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    continue

                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = emotion_classifier.predict(gray_face)
                emotion_probability = np.max(emotion_prediction)
                emotion_label_arg = np.argmax(emotion_prediction)
                emotion_text = emotion_labels[emotion_label_arg]
                emotion_window.append(emotion_text)

                if len(emotion_window) > frame_window:
                    emotion_window.pop(0)
                try:
                    emotion_mode = mode(emotion_window)
                except:
                    continue
                
                
                if emotion_text == 'angry':
                    angry += 1
                    color = emotion_probability * np.asarray((255, 0, 0))
                elif emotion_text == 'sad':
                    sad += 1
                    color = emotion_probability * np.asarray((0, 0, 255))
                elif emotion_text == 'happy':
                    happy += 1
                    color = emotion_probability * np.asarray((255, 255, 0))
                elif emotion_text == 'surprise':
                    surprise += 1
                    color = emotion_probability * np.asarray((0, 255, 255))
                elif emotion_text == 'disgust':
                    disgust += 1
                    color = emotion_probability * np.asarray((0, 255, 255))
                elif emotion_text == 'fear':
                    fear += 1
                    color = emotion_probability * np.asarray((0, 255, 255))
                else:
                    neutral += 1
                    color = emotion_probability * np.asarray((0, 255, 0))

                color = color.astype(int)
                color = color.tolist()

                draw_bounding_box(face_utils.rect_to_bb(face_coordinates), rgb_image, color)
                draw_text(face_utils.rect_to_bb(face_coordinates), rgb_image, emotion_mode,
                        color, 0, -45, 1, 1)
                
                print(angry, disgust, fear, happy, neutral, sad,surprise)
        except Exception as e:
            print("Error:", e)
            break
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('window_frame', bgr_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return angry, disgust, fear, happy, neutral, sad, surprise

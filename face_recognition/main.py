import os.path
import pickle
import tkinter as tk
import cv2
import util
import datetime
from PIL import Image, ImageTk
import face_recognition
import sys

from Silent_Face_Anti_Spoofing.test import test

sys.path.append(os.path.dirname(__file__))
    

class App:
    def __init__(self):
        self.main_window = tk.Tk()  
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x = 750, y = 300)

        self.register_button_main_window = util.get_button(self.main_window, 'Register', 'grey', self.register_new_user, fg = 'black')
        self.register_button_main_window.place(x = 750, y = 400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x = 10 , y = 0, width = 700, height = 500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label

        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image = imgtk)

        self._label.after(20, self.process_webcam)




    def login(self):
        label = test(image =self.most_recent_capture_arr,
                model_dir = '/home/zoro/Desktop/Face-Recognition/face_recognition/Silent_Face_Anti_Spoofing/resources/anti_spoof_models',
                device_id = 0
                )
        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Opps....', 'Unknown User. Please register first or try again')
            else:
                util.msg_box('Welcome Back !', 'Welcome, {}.'.format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{},{}\n'.format(name, datetime.datetime.now()))
                    f.close()   

        else:
            util.msg_box('Hey, you are spoofer!','You are fake Bruh!!')

        



    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=200)
        self.tryagain_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.reset_register_new_user_window)
        self.tryagain_button_register_new_user_window.place(x=750, y=300)
        self.back_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Back', 'grey',self.close_register_new_user_window)
        self.back_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x = 750, y = 80)


        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,'Enter Username')
        self.text_label_register_new_user.place(x = 750, y = 40)
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image = imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def reset_register_new_user_window(self):
        # Function to reset the registration window
        self.register_new_user_window.destroy()
        self.register_new_user()

    def close_register_new_user_window(self):
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        # Get face encodings
        face_encodings_list = face_recognition.face_encodings(self.register_new_user_capture)

        if len(face_encodings_list) > 0:
            # Take the first face encoding in the list
            embeddings = face_encodings_list[0]

            # Save the face embedding to a file
            file_path = os.path.join(self.db_dir, '{}.pickle'.format(name))
            with open(file_path, 'wb') as file:
                pickle.dump(embeddings, file)

            util.msg_box('Success!', 'User registered successfully!')
            self.register_new_user_window.destroy()
        else:
            util.msg_box('Error', 'No face detected. Please try again.')


if __name__ == "__main__":
    app = App()
    app.start()
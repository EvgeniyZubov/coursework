import tkinter as tk
from tkinter import Menu, filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np

class VideoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("cw-322-v01-Zubov-Evgen")
        self.geometry("980x480")
        self.configure(bg="#2e3b4e")
        self.video_source = None
        self.cap = None
        self.delay = 15
        self.create_widgets()

    def create_widgets(self):
        # Меню
        menubar = Menu(self,bg='#3b4f68', fg='#ffffff')
        file_menu = Menu(menubar, tearoff=0, bg='#3b4f68', fg='#ffffff')
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        # Джерело відеозображення
        self.source_var = tk.StringVar(value="Webcam")
        source_menu = tk.OptionMenu(self, self.source_var, "Webcam", "Video file", command=self.select_source)
        source_menu.config(bg='#3b4f68', fg='#ffffff', font=('Arial', 10))
        source_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Фільтри-чекбокси
        self.rgb_var = tk.IntVar()
        self.shift_var = tk.IntVar()
        self.prewitt_var = tk.IntVar()
        self.highpass_var = tk.IntVar()

        tk.Checkbutton(self, text="RGB", variable=self.rgb_var,bg='#2e3b4e', fg='#ffffff', font=('Arial', 10)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Checkbutton(self, text="Вертикальне зміщення", variable=self.shift_var, command=self.toggle_shift_input,bg='#2e3b4e', fg='#ffffff', font=('Arial', 10)).grid(row=1, column=1, sticky="w", padx=5)
        tk.Checkbutton(self, text="Границя Превітта", variable=self.prewitt_var, command=self.toggle_prewitt_slider,bg='#2e3b4e', fg='#ffffff', font=('Arial', 10)).grid(row=1, column=2, sticky="w", padx=5)
        tk.Checkbutton(self, text="Фільтр ВЧ", variable=self.highpass_var, command=self.toggle_highpass_sliders,bg='#2e3b4e', fg='#ffffff', font=('Arial', 10)).grid(row=1, column=3, sticky="w", padx=5)

        # Поле для вертикального зміщення
        self.shift_value_var = tk.StringVar(value="30")
        self.shift_entry = tk.Entry(self, textvariable=self.shift_value_var, width=8)
        self.shift_entry.grid(row=1, column=4, sticky="w")
        self.shift_entry.grid_remove()

        # повзунок для Превітта
        self.prewitt_slider = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, label="Порог Превитта", bg='#2e3b4e', fg='#ffffff')
        self.prewitt_slider.set(100)
        self.prewitt_slider.grid(row=2, column=0, columnspan=2, sticky="we", padx=5)
        self.prewitt_slider.grid_remove()

        # Повзунки для фільтра ВЧ
        self.hp_slider1 = tk.Scale(self, from_=0, to=255, resolution=1, orient=tk.HORIZONTAL, label="Значення порогу", bg='#2e3b4e', fg='#ffffff')
        self.hp_slider2 = tk.Scale(self, from_=0, to=50, resolution=1, orient=tk.HORIZONTAL, label="Центральне число ядра", bg='#2e3b4e', fg='#ffffff')
        self.hp_slider3 = tk.Scale(self, from_=0, to=10, resolution=0.5, orient=tk.HORIZONTAL, label="Крайнє число ядра", bg='#2e3b4e', fg='#ffffff')

        self.hp_slider1.set(1.0)
        self.hp_slider2.set(1.0)
        self.hp_slider3.set(1.0)

        self.hp_slider1.grid(row=2, column=2, sticky="we", padx=5)
        self.hp_slider2.grid(row=2, column=3, sticky="we", padx=5)
        self.hp_slider3.grid(row=2, column=4, sticky="we", padx=5)

        self.hp_slider1.grid_remove()
        self.hp_slider2.grid_remove()
        self.hp_slider3.grid_remove()

        # Канваси
        self.source_canvas = tk.Canvas(self, width=400, height=300, bg='black')
        self.output_canvas = tk.Canvas(self, width=400, height=300, bg='black')
        self.source_canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.output_canvas.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

    def toggle_shift_input(self):
        if self.shift_var.get():
            self.shift_entry.grid()
        else:
            self.shift_entry.grid_remove()

    def toggle_prewitt_slider(self):
        if self.prewitt_var.get():
            self.prewitt_slider.grid()
        else:
            self.prewitt_slider.grid_remove()

    def toggle_highpass_sliders(self):
        if self.highpass_var.get():
            self.hp_slider1.grid()
            self.hp_slider2.grid()
            self.hp_slider3.grid()
        else:
            self.hp_slider1.grid_remove()
            self.hp_slider2.grid_remove()
            self.hp_slider3.grid_remove()

    def select_source(self, choice):
        if choice == "Webcam":
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
            self.video_source = 0
        elif choice == "Video file":
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
            file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
            if file_path:
                self.video_source = file_path
        self.start_video()

    def start_video(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(self.video_source)
        self.filter_frame()

        if self._after_id:
            self.after_cancel(self._after_id)
        self.filter_frame()

    def filter_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                output = frame_rgb.copy()

                # RGB вимикає конвертацию у градієнти сірого
                if not self.rgb_var.get():
                    output = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
                    output = cv2.cvtColor(output, cv2.COLOR_GRAY2RGB)

                # Вертикальне зміщення
                if self.shift_var.get():
                    try:
                        shift = int(self.shift_value_var.get())
                        output = np.roll(output, shift, axis=0)
                    except ValueError:
                        pass

                # Превітт
                if self.prewitt_var.get():
                    gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
                    kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
                    edge = cv2.filter2D(gray, -1, kernel)
                    _, thresh = cv2.threshold(edge, self.prewitt_slider.get(), 255, cv2.THRESH_BINARY)
                    output = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

                # Фильтр ВЧ (зі змінними параметрами)
                if self.highpass_var.get():
                    center_val = int(self.hp_slider2.get())
                    edge_val = int(self.hp_slider3.get())
                    thresh_value = int(self.hp_slider1.get())

                    kernel_sharp = np.array([[-edge_val, -edge_val, -edge_val],  # Ядро фільтра ВЧ
                                             [-edge_val, center_val, -edge_val],
                                             [-edge_val, -edge_val, -edge_val]])

                    output = cv2.filter2D(output, -1, kernel_sharp)  # Інвертування кольорів для відображення вищих частот

                    _, output = cv2.threshold(output, thresh_value, 255, cv2.THRESH_BINARY)

                img1 = ImageTk.PhotoImage(Image.fromarray(frame_rgb).resize((400, 300)))
                img2 = ImageTk.PhotoImage(Image.fromarray(output).resize((400, 300)))

                self.source_canvas.create_image(0, 0, anchor=tk.NW, image=img1)
                self.output_canvas.create_image(0, 0, anchor=tk.NW, image=img2)

                self.source_canvas.image = img1
                self.output_canvas.image = img2
            self._after_id = self.after(self.delay, self.filter_frame)


if __name__ == "__main__":
    app = VideoApp()
    app.mainloop()

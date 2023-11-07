import tkinter as tk
import subprocess
import threading
from queue import Queue
import os
import shutil
import requests
import zipfile

# Create a function to be executed when the subprocess button is clicked

if not os.path.exists(".\\Binaries"):
    os.mkdir(".\\Binaries")
    r = requests.get('https://github.com/yt-dlp/yt-dlp/releases/download/2023.10.13/yt-dlp.exe', allow_redirects=True)
    open('.\\Binaries\\yt-dlp.exe', 'wb').write(r.content)
    r = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip", allow_redirects=True)
    open('.\\Binaries\\ffmpeg.zip', 'wb').write(r.content)
    with zipfile.ZipFile(".\\Binaries\\ffmpeg.zip", "r") as zip_ref:
        zip_ref.extractall(".\\Binaries\\ffmpeg")
    os.rename(".\\Binaries\\ffmpeg\\ffmpeg-6.0-essentials_build\\bin\\ffmpeg.exe", ".\\Binaries\\ffmpeg.exe")
    shutil.rmtree(".\\Binaries\\ffmpeg")
    os.remove(".\\Binaries\\ffmpeg.zip")

if not os.path.exists(".\\Downloads"):
    os.mkdir(".\\Downloads")


def update():
    subprocess.run([".\\binaries\\yt-dlp.exe", "-U"])


def run_subprocess1():
    url = command_entry.get()
    thread = threading.Thread(target=thead_run_subprocess1, args=(url,))
    thread.start()


def thead_run_subprocess1(url):
    try:
        process = subprocess.Popen(
            [".\\binaries\\yt-dlp.exe", "-f", """ (bv*[vcodec~='^((he|a)vc|h26[45])']+ba[ext=m4a]) """, "-o",
             ".\\Downloads\\%(title)s.%(ext)s", str(url)], shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
        log_queue.put("DOWNLOAD FINISHED")
    except Exception as e:
        log_queue.put(f"Subprocess error: {str(e)}")


def run_subprocess2():
    url = command_entry.get()
    thread = threading.Thread(target=thead_run_subprocess2, args=(url,))
    thread.start()


def thead_run_subprocess2(url):
    try:
        process = subprocess.Popen(
            [".\\binaries\\yt-dlp.exe", "-o",
             ".\\Downloads\\%(title)s.%(ext)s", str(url)], shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
        log_queue.put("DOWNLOAD FINISHED")
    except Exception as e:
        log_queue.put(f"Subprocess error: {str(e)}")


def run_subprocess3():
    url = command_entry.get()
    thread = threading.Thread(target=thead_run_subprocess3, args=(url,))
    thread.start()


def thead_run_subprocess3(url):
    try:
        process = subprocess.Popen(
            [".\\binaries\\yt-dlp.exe", "--ffmpeg-location", ".\\binaries\\ffmpeg.exe",
             "--recode-video", "mp4", "-o",
             ".\\Downloads\\%(title)s.%(ext)s", str(url)], shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
        log_queue.put("DOWNLOAD FINISHED")
    except Exception as e:
        log_queue.put(f"Subprocess error: {str(e)}")


def run_subprocess4():
    url = command_entry.get()
    thread = threading.Thread(target=thead_run_subprocess4, args=(url,))
    thread.start()


def thead_run_subprocess4(url):
    try:
        process = subprocess.Popen(
            [".\\binaries\\yt-dlp.exe", "--ffmpeg-location", ".\\binaries\\ffmpeg.exe",
             "-x", "--audio-format", "mp3", "--audio-quality", "0", "-o",
             ".\\Downloads\\%(title)s.%(ext)s", str(url)], shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
        log_queue.put("DOWNLOAD FINISHED")
    except Exception as e:
        log_queue.put(f"Subprocess error: {str(e)}")


def update_log_text():
    while True:
        log_message = log_queue.get()
        if log_message is None:
            break
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, log_message)
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

# Create the main application window
app = tk.Tk()
app.title("Download Everything.")
app.geometry("700x600")

# Create an Entry widget for the user to enter a command with a placeholder text
command_entry = tk.Entry(app, font=("Helvetica", 12))
command_entry.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="nsew")
command_entry.insert(0, "Put the URL here")  # Add placeholder text

# Create four buttons to run the subprocess, arrange them in the middle
button_padding = (5, 2)  # Adjust the button height by changing the pady value
subprocess_button1 = tk.Button(app, text="Download best MP4", command=run_subprocess1, font=("Helvetica", 12), padx=button_padding[0], pady=button_padding[1])
subprocess_button2 = tk.Button(app, text="Download best Quality", command=run_subprocess2, font=("Helvetica", 12), padx=button_padding[0], pady=button_padding[1])
subprocess_button3 = tk.Button(app, text="Download best Quality and Convert to mp4", command=run_subprocess3, font=("Helvetica", 12), padx=button_padding[0], pady=button_padding[1])
subprocess_button4 = tk.Button(app, text="Download Audio as MP3", command=run_subprocess4, font=("Helvetica", 12), padx=button_padding[0], pady=button_padding[1])

subprocess_button1.grid(row=1, column=0, sticky="nsew")
subprocess_button2.grid(row=1, column=1, sticky="nsew")
subprocess_button3.grid(row=2, column=0, sticky="nsew")
subprocess_button4.grid(row=2, column=1, sticky="nsew")

# Create a Text widget for displaying the subprocess output (at the bottom)
log_text = tk.Text(app, font=("Helvetica", 12), height=10)
log_text.grid(row=3, column=0, columnspan=2, pady=(10, 20), sticky="nsew")

# Configure row and column weights
for i in range(4):
    app.columnconfigure(i, weight=1)
for i in range(4):
    app.rowconfigure(i, weight=1)

log_queue = Queue()

# Create a separate thread to update the log text widget
log_thread = threading.Thread(target=update_log_text)
log_thread.daemon = True
log_thread.start()

# Start the Tkinter main loop
threading.Thread(target=update).start()
app.mainloop()

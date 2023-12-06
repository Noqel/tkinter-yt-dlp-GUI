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
    r = requests.get("https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-6.0-essentials_build.zip", allow_redirects=True)
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
    thread = threading.Thread(target=thread_run_subprocess1, args=(url,))
    thread.start()


def thread_run_subprocess1(url):
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
    thread = threading.Thread(target=thread_run_subprocess2, args=(url,))
    thread.start()


def thread_run_subprocess2(url):
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
    thread = threading.Thread(target=thread_run_subprocess3, args=(url,))
    thread.start()


def thread_run_subprocess3(url):
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
    thread = threading.Thread(target=thread_run_subprocess4, args=(url,))
    thread.start()


def thread_run_subprocess4(url):
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


def run_subprocess5():
    url = command_entry.get()
    thread = threading.Thread(target=thread_run_subprocess5, args=(url,))
    thread.start()


def thread_run_subprocess5(url):
    os.mkdir("temp")
    try:
        process = subprocess.Popen(
            [".\\binaries\\yt-dlp.exe", "-o",
             ".\\temp\\video.mp4", str(url)], shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
        log_queue.put("DOWNLOAD FINISHED")
    except Exception as e:
        log_queue.put(f"Subprocess error: {str(e)}")
    try:
        process = subprocess.Popen(
            [".\\binaries\\ffmpeg.exe", "-i",
             ".\\temp\\video.mp4", "-vf", "select='gt(scene,0.3)',showinfo",
             "-vsync", "vfr", "-q:v", "2", "-f", "image2",
             "-start_number", "0", "temp/%03d.png"], shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            log_queue.put(line)
        process.stdout.close()
        process.wait()
        log_queue.put("DOWNLOAD FINISHED")
    except Exception as e:
        log_queue.put(f"Subprocess error: {str(e)}")
    shutil.copy("./temp/000.png", "./Downloads/picture.png")
    shutil.rmtree(".\\temp")
    os.startfile(".\\Downloads\\picture.png")


def run_subprocess6():
    url = command_entry.get()
    thread = threading.Thread(target=thread_run_subprocess6, args=(url,))
    thread.start()


def thread_run_subprocess6(url):
    # Create a new popup window
    popup_window = tk.Toplevel(app)
    popup_window.title("Crunchyroll Downloader")

    # Create three labels for the text fields
    labels = ["URL:", "USER-AGENT:", "BROWSER:"]
    for i, label_text in enumerate(labels):
        label = tk.Label(popup_window, text=label_text, font=("Helvetica", 12))
        label.grid(row=i, column=0, pady=(10, 0), padx=10, sticky="w")

    # Create three entry widgets for user input
    input_entries = [tk.Entry(popup_window, font=("Helvetica", 12)) for _ in range(3)]
    for i, entry in enumerate(input_entries):
        entry.grid(row=i, column=1, pady=(10, 0), padx=10, sticky="ew")

    # Create a submit button in the popup window
    submit_button = tk.Button(popup_window, text="Submit", command=lambda: on_submit(input_entries, popup_window),
                              font=("Helvetica", 12))
    submit_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="nsew")


def on_submit(input_entries, popup_window):
    thread = threading.Thread(target=thread_on_submit, args=(str(input_entries[0].get()), str(input_entries[1].get()), str(input_entries[2].get())))
    thread.start()
    popup_window.destroy()


def thread_on_submit(url, user_agent, browser):
    try:
        process = subprocess.Popen(
            [".\\binaries\\yt-dlp.exe", "--ffmpeg-location", ".\\binaries\\ffmpeg.exe",
             "--user-agent", user_agent, "-o",
             ".\\Downloads\\%(title)s.%(ext)s",
             "--cookies-from-browser", browser, url], shell=True, stdout=subprocess.PIPE,
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
subprocess_button5 = tk.Button(app, text="Spicy Button", command=run_subprocess5, font=("Helvetica", 12), padx=button_padding[0], pady=button_padding[1])
subprocess_button6 = tk.Button(app, text="Crunchyroll", command=run_subprocess6, font=("Helvetica", 12), padx=button_padding[0], pady=button_padding[1])

subprocess_button1.grid(row=1, column=0, sticky="nsew")
subprocess_button2.grid(row=1, column=1, sticky="nsew")
subprocess_button3.grid(row=2, column=0, sticky="nsew")
subprocess_button4.grid(row=2, column=1, sticky="nsew")
subprocess_button5.grid(row=3, column=0, sticky="nsew")
subprocess_button6.grid(row=3, column=1, sticky="nsew")

# Create a Text widget for displaying the subprocess output (at the bottom)
log_text = tk.Text(app, font=("Helvetica", 12), height=10)
log_text.grid(row=4, column=0, columnspan=2, pady=(10, 20), sticky="nsew")

# Configure row and column weights
for i in range(5):
    app.columnconfigure(i, weight=1)
for i in range(5):
    app.rowconfigure(i, weight=1)

log_queue = Queue()

# Create a separate thread to update the log text widget
log_thread = threading.Thread(target=update_log_text)
log_thread.daemon = True
log_thread.start()

# Start the Tkinter main loop
threading.Thread(target=update).start()
app.mainloop()

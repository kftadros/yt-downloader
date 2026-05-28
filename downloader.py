import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

try:
    import yt_dlp
except ImportError:
    messagebox.showerror("Missing Library", "Run: pip install yt-dlp")
    exit()


class Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x550")
        self.root.resizable(True, True)
        self.root.configure(bg="#1a1a2e")

        self.download_path = os.path.expanduser("~/Downloads")
        self.format_var = tk.StringVar(value="mp3")
        self.quality_var = tk.StringVar(value="best")

        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="YouTube Downloader",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        )
        title.pack(pady=20)

        # URL Entry
        url_frame = tk.Frame(self.root, bg="#1a1a2e")
        url_frame.pack(padx=30, fill="x")

        tk.Label(
            url_frame,
            text="YouTube URL:",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white"
        ).pack(anchor="w")

        self.url_entry = tk.Entry(
            url_frame,
            font=("Arial", 12),
            bg="#16213e",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=5
        )
        self.url_entry.pack(fill="x", ipady=8, pady=5)

        # Format Selection
        format_frame = tk.Frame(self.root, bg="#1a1a2e")
        format_frame.pack(padx=30, fill="x", pady=10)

        tk.Label(
            format_frame,
            text="Format:",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white"
        ).pack(side="left", padx=(0, 10))

        mp3_btn = tk.Radiobutton(
            format_frame,
            text="MP3 (Audio)",
            variable=self.format_var,
            value="mp3",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white",
            selectcolor="#16213e",
            activebackground="#1a1a2e",
            activeforeground="white"
        )
        mp3_btn.pack(side="left", padx=10)

        mp4_btn = tk.Radiobutton(
            format_frame,
            text="MP4 (Video)",
            variable=self.format_var,
            value="mp4",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white",
            selectcolor="#16213e",
            activebackground="#1a1a2e",
            activeforeground="white"
        )
        mp4_btn.pack(side="left", padx=10)

        # Quality Selection
        quality_frame = tk.Frame(self.root, bg="#1a1a2e")
        quality_frame.pack(padx=30, fill="x", pady=5)

        tk.Label(
            quality_frame,
            text="Quality (MP4 only):",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white"
        ).pack(side="left", padx=(0, 10))

        for q in ["best", "1080p", "720p", "480p", "360p"]:
            tk.Radiobutton(
                quality_frame,
                text=q,
                variable=self.quality_var,
                value=q,
                font=("Arial", 10),
                bg="#1a1a2e",
                fg="white",
                selectcolor="#16213e",
                activebackground="#1a1a2e",
                activeforeground="white"
            ).pack(side="left", padx=5)

        # Save Location
        path_frame = tk.Frame(self.root, bg="#1a1a2e")
        path_frame.pack(padx=30, fill="x", pady=5)

        tk.Label(
            path_frame,
            text="Save to:",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white"
        ).pack(anchor="w")

        path_row = tk.Frame(path_frame, bg="#1a1a2e")
        path_row.pack(fill="x")

        self.path_label = tk.Label(
            path_row,
            text=self.download_path,
            font=("Arial", 10),
            bg="#16213e",
            fg="#aaaaaa",
            anchor="w",
            padx=5
        )
        self.path_label.pack(side="left", fill="x", expand=True, ipady=6)

        browse_btn = tk.Button(
            path_row,
            text="Browse",
            font=("Arial", 10),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            command=self.browse_folder
        )
        browse_btn.pack(side="right", padx=(5, 0), ipady=6)

        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            mode="indeterminate",
            length=540
        )
        self.progress.pack(pady=15)

        # Status Label
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#aaaaaa"
        )
        self.status_label.pack()

        # Download Button
        self.download_btn = tk.Button(
            self.root,
            text="Download",
            font=("Arial", 14, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=30,
            pady=10,
            command=self.start_download
        )
        self.download_btn.pack(pady=15)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.path_label.config(text=folder)

    def start_download(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning("Missing URL", "Please enter a YouTube URL.")
            return

        # Run download in separate thread so UI doesn't freeze
        self.download_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Downloading...")

        thread = threading.Thread(target=self.download, args=(url,))
        thread.start()

    def download(self, url):
        fmt = self.format_var.get()

        if fmt == "mp3":
            options = {
                "format": "bestaudio/best",
                "outtmpl": f"{self.download_path}/%(title)s_%(autonumber)s.%(ext)s",
                "overwrites": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
        else:
            quality = self.quality_var.get()
            if quality == "best":
                fmt = "bestvideo+bestaudio/best"
            else:
                height = quality.replace("p", "")
                fmt = f"bestvideo[height<={height}]+bestaudio/best"
            
            options = {
                "format": fmt,
                "outtmpl": f"{self.download_path}/%(title)s_%(autonumber)s.%(ext)s",
                "merge_output_format": "mp4",
                "overwrites": True,
            }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
            self.on_success()
        except Exception as e:
            self.on_error(str(e))

    def on_success(self):
        self.progress.stop()
        self.status_label.config(text="Download complete!", fg="#00ff88")
        self.download_btn.config(state="normal")
        messagebox.showinfo("Done", f"Saved to: {self.download_path}")

    def on_error(self, error):
        self.progress.stop()
        self.status_label.config(text="Download failed.", fg="#e94560")
        self.download_btn.config(state="normal")
        messagebox.showerror("Error", f"Something went wrong:\n{error}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Downloader(root)
    root.mainloop()
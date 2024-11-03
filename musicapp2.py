import tkinter as tk
from tkinter import messagebox, Listbox, StringVar, Frame, VERTICAL, Scrollbar, ttk
import pygame
import random
from tkinter import filedialog
import os

class ModernMusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern Music Player")
        self.master.geometry("800x600")
        self.master.configure(bg='#121212')  # Spotify's dark background
        
        # Initialize Pygame Mixer
        pygame.mixer.init()
        
        self.playlist = []
        self.current_song = None
        self.is_playing = False
        
        self.create_gui()
        self.apply_styles()
        
    def create_gui(self):
        # Main container
        self.main_frame = Frame(self.master, bg='#121212')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top section - Logo and search
        self.top_frame = Frame(self.main_frame, bg='#121212')
        self.top_frame.pack(fill='x', pady=(0, 20))
        
        self.title_label = tk.Label(self.top_frame, text="🎵 Modern Music Player", 
                                  font=('Helvetica', 24, 'bold'), 
                                  bg='#121212', fg='#FFFFFF')
        self.title_label.pack(side='left')
        
        # Browse button
        self.browse_button = tk.Button(self.top_frame, text="Browse Files", 
                                     command=self.browse_files,
                                     font=('Helvetica', 10),
                                     bg='#282828', fg='#FFFFFF',
                                     activebackground='#404040',
                                     activeforeground='#FFFFFF',
                                     relief='flat',
                                     padx=20)
        self.browse_button.pack(side='right', pady=5)
        
        # Middle section - Playlist
        self.playlist_frame = Frame(self.main_frame, bg='#282828')
        self.playlist_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Custom style for the playlist
        self.playlist_box = Listbox(self.playlist_frame,
                                  bg='#282828',
                                  fg='#FFFFFF',
                                  selectbackground='#404040',
                                  selectforeground='#FFFFFF',
                                  font=('Helvetica', 10),
                                  relief='flat',
                                  height=15)
        self.playlist_box.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.scrollbar = Scrollbar(self.playlist_frame, orient=VERTICAL,
                                 command=self.playlist_box.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.playlist_box.config(yscrollcommand=self.scrollbar.set)
        
        # Bottom section - Controls
        self.control_frame = Frame(self.main_frame, bg='#282828')
        self.control_frame.pack(fill='x', pady=(0, 10))
        
        # Now Playing Label
        self.now_playing_var = StringVar()
        self.now_playing_var.set("No song playing")
        self.now_playing_label = tk.Label(self.control_frame,
                                        textvariable=self.now_playing_var,
                                        bg='#282828', fg='#B3B3B3',
                                        font=('Helvetica', 10))
        self.now_playing_label.pack(pady=5)
        
        # Control Buttons Frame
        self.buttons_frame = Frame(self.control_frame, bg='#282828')
        self.buttons_frame.pack(pady=10)
        
        # Control Buttons
        button_configs = [
            ("⏮", self.previous_song, "#1DB954"),  # Previous
            ("⏯", self.play_pause_song, "#1DB954"),  # Play/Pause
            ("⏹", self.stop_song, "#1DB954"),  # Stop
            ("⏭", self.next_song, "#1DB954"),  # Next
            ("🔀", self.shuffle_playlist, "#1DB954"),  # Shuffle
        ]
        
        for symbol, command, color in button_configs:
            btn = tk.Button(self.buttons_frame, text=symbol,
                          command=command,
                          font=('Helvetica', 16),
                          bg='#282828', fg=color,
                          activebackground='#404040',
                          activeforeground=color,
                          relief='flat',
                          width=3, height=1)
            btn.pack(side='left', padx=10)
            
        # Volume control
        self.volume_frame = Frame(self.control_frame, bg='#282828')
        self.volume_frame.pack(pady=5)
        
        self.volume_label = tk.Label(self.volume_frame, text="🔊",
                                   bg='#282828', fg='#FFFFFF')
        self.volume_label.pack(side='left', padx=5)
        
        self.volume_scale = ttk.Scale(self.volume_frame,
                                    from_=0, to=100,
                                    orient='horizontal',
                                    command=self.set_volume,
                                    length=200)
        self.volume_scale.set(70)  # Default volume
        self.volume_scale.pack(side='left', padx=5)
        
    def apply_styles(self):
        style = ttk.Style()
        style.configure("TScale",
                       background='#282828',
                       troughcolor='#404040',
                       slidercolor='#1DB954')
        
    def browse_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg"),
                ("All Files", "*.*")
            ]
        )
        for file in files:
            self.add_song(file)
    
    def add_song(self, song_path):
        if song_path:
            self.playlist.append(song_path)
            self.playlist_box.insert(tk.END, os.path.basename(song_path))
    
    def play_pause_song(self):
        if not self.is_playing:
            try:
                if not pygame.mixer.music.get_busy():
                    selected_index = self.playlist_box.curselection()[0]
                    song_path = self.playlist[selected_index]
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()
                    self.current_song = selected_index
                    self.now_playing_var.set(f"Now Playing: {os.path.basename(song_path)}")
                else:
                    pygame.mixer.music.unpause()
                self.is_playing = True
            except (IndexError, pygame.error) as e:
                messagebox.showerror("Error", "Please select a valid song to play!")
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
    
    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.now_playing_var.set("No song playing")
    
    def previous_song(self):
        if self.current_song is not None and self.current_song > 0:
            self.current_song -= 1
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_song)
            self.playlist_box.see(self.current_song)
            self.play_pause_song()
    
    def next_song(self):
        if self.current_song is not None and self.current_song < len(self.playlist) - 1:
            self.current_song += 1
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_song)
            self.playlist_box.see(self.current_song)
            self.play_pause_song()
    
    def shuffle_playlist(self):
        if self.playlist:
            current_selection = None
            if self.playlist_box.curselection():
                current_selection = self.playlist_box.get(self.playlist_box.curselection())
            
            combined = list(zip(self.playlist, [self.playlist_box.get(i) for i in range(self.playlist_box.size())]))
            random.shuffle(combined)
            self.playlist[:], display_names = zip(*combined)
            
            self.playlist_box.delete(0, tk.END)
            for name in display_names:
                self.playlist_box.insert(tk.END, name)
            
            if current_selection:
                for i in range(self.playlist_box.size()):
                    if self.playlist_box.get(i) == current_selection:
                        self.playlist_box.selection_set(i)
                        self.current_song = i
                        break
    
    def set_volume(self, value):
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#121212')
    app = ModernMusicPlayer(root)
    root.mainloop()
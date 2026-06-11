import os
import time
import queue
import threading
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from ui import build_ui as ui_maker

from decoder import load_and_decode
from tracker import contact_tracker,get_peer_list
from downloader import download_and_save
from progress_manager import load_progress
from assemble_file import assemble_file


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TextRedirect:

    def __init__(self,q):
        self.q=q

    def write(self,text):
        if text.strip():
            self.q.put(text)

    def flush(self):
        pass



class TorrentGUI(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("P2P Network Torrent Client")
        self.geometry("1600x1050")

        self.torr_dict=None
        self.num_pieces=0
        self.start_time=None

        self.log_queue=queue.Queue()
        self.piece_boxes=[]

        self.build_ui()

        self.after(250,self.poll_logs)
        self.after(1000,self.refresh_progress)


    ##################################################

    def build_ui(self):
        ui_maker(self)
    ##################################################

    def open_torrent(self):

        path=filedialog.askopenfilename(
            filetypes=[("Torrent Files","*.torrent")]
        )

        if not path:
            return

        self.torr_dict=load_and_decode(path)

        pieces=self.torr_dict[b'info'][b'pieces']
        self.num_pieces=len(pieces)//20

        name=self.torr_dict[b'info'][b'name'].decode()

        if b'length' in self.torr_dict[b'info']:
            length=self.torr_dict[b'info'][b'length']
        else:
            length=sum(
                f[b'length']
                for f in self.torr_dict[b'info'][b'files']
            )

        mib=int(length/(1024*1024))

        self.meta_label.configure(
text=
f"""File:
{name}

Size:
{mib} MiB

Pieces:
{self.num_pieces}
"""
        )

        self.make_piece_grid()



    ###################################################

    def make_piece_grid(self):

        for w in self.piece_frame.winfo_children():
            w.destroy()

        self.piece_boxes=[]

        self.piece_frame.update_idletasks()

        # actual visible width of scrollable area
        frame_width = self.piece_frame.winfo_width()

        box_size = 10
        pad = 2   # padx=1 on each side

        cell = box_size + pad

        # calculate how many fit
        cols = max(1, frame_width // cell - 5)


        for i in range(self.num_pieces):

            box = ctk.CTkLabel(
                self.piece_frame,
                text="",
                width=box_size,
                height=box_size,
                fg_color="#d0d0d0"
            )

            box.grid(
                row=i // cols,
                column=i % cols,
                padx=1,
                pady=1
            )

            self.piece_boxes.append(box)
            
    ###################################################

    def start_download_thread(self):

        threading.Thread(
            target=self.run_download,
            daemon=True
        ).start()



    def run_download(self):

        import sys
        sys.stdout=TextRedirect(self.log_queue)

        self.start_time=time.time()

        self.status_label.configure(
            text="Status: Contacting Tracker"
        )

        peer_id=b'-PC0001-'+os.urandom(12)

        if b'length' in self.torr_dict[b'info']:
            total_length=self.torr_dict[b'info'][b'length']
        else:
            total_length=sum(
                f[b'length']
                for f in self.torr_dict[b'info'][b'files']
            )

        info_hash,tracker_response=contact_tracker(
            peer_id,
            self.torr_dict,
            total_length
        )

        peer_list=get_peer_list(
            tracker_response[b'peers']
        )

        self.stats_label.configure(
text=
f"""
Seeders: {tracker_response[b'complete']}
Leechers: {tracker_response[b'incomplete']}
Peers Connected: {len(peer_list)}
Downloaded: {tracker_response[b'downloaded']}
"""
        )


        self.peer_box.delete("0.0","end")

        for p in peer_list[:30]:
            self.peer_box.insert(
                "end",
                f"{p}   Active\n"
            )

        self.status_label.configure(
            text="Status: Downloading"
        )


        download_and_save(
            self.num_pieces,
            peer_list,
            peer_id,
            info_hash,
            self.torr_dict[b'info'][b'piece length'],
            self.torr_dict[b'info'][b'pieces'],
            self.torr_dict[b'info'][b'name'].decode(),
            total_length=total_length
        )


        self.status_label.configure(
            text="Status: Assembling"
        )

        assemble_file(
            self.num_pieces,
            self.torr_dict[b'info'][b'name'].decode(),
            output_path="output",
            final_output="output file"
        )

        self.status_label.configure(
            text="Status: Download Complete"
        )



    ###################################################

    def refresh_progress(self):

        try:

            if self.torr_dict:

                total,downloaded=load_progress(
                    self.torr_dict[b'info'][b'name'].decode()
                )

                if total:

                    pct=len(downloaded)/total

                    self.progressbar.set(pct)

                    self.progress_label.configure(
                        text=f"{len(downloaded)}/{total} ({pct*100:.2f}%)"
                    )

                    for i in downloaded:
                        if i<len(self.piece_boxes):
                            self.piece_boxes[i].configure(
                                fg_color="#58b52c"
                            )


                if self.start_time:

                    elapsed=int(
                        time.time()-self.start_time
                    )

                    mins=elapsed//60
                    secs=elapsed%60

                    self.timer_label.configure(
                        text=f"Elapsed\n{mins:02}:{secs:02}"
                    )

        except:
            pass


        self.after(
            1000,
            self.refresh_progress
        )



    ###################################################

    def poll_logs(self):

        while not self.log_queue.empty():

            msg=self.log_queue.get()

            self.logbox.insert(
                "end",
                msg+"\n"
            )

            self.logbox.see("end")

        self.after(250,self.poll_logs)



if __name__=="__main__":

    app=TorrentGUI()
    app.mainloop()
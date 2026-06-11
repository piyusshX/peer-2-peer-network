import customtkinter as ctk
from PIL import Image


def build_ui(self):

    BG = "white"
    PANEL = "#f5f6f8"
    PANEL2 = "#eef1f4"
    BORDER = "#d7dbe0"
    DARK_PANEL = "#20242b"

    self.configure(fg_color=BG)

    ##################################################
    # ROOT LAYOUT
    ##################################################

    self.grid_rowconfigure(0, weight=0)
    self.grid_rowconfigure(1, weight=3)
    self.grid_rowconfigure(2, weight=2)
    self.grid_rowconfigure(3, weight=0)
    self.grid_columnconfigure(0, weight=1)


    ##################################################
    # TOP TOOLBAR
    ##################################################

    top = ctk.CTkFrame(
        self,
        fg_color=BG,
        corner_radius=10,
        border_width=1,
        border_color=BORDER,
        height=62
    )
    top.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=6,
        pady=(6,3)
    )
    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=0)
    top.grid_rowconfigure(0, weight=1)
    top.grid_rowconfigure(1, weight=0)
    top.grid_propagate(False)


    left_toolbar = ctk.CTkFrame(top, fg_color=BG)
    left_toolbar.grid(
        row=0,
        column=0,
        sticky="w",
        padx=8,
        pady=6
    )

    for txt,cmd,w in [
        ("Open Torrent",self.open_torrent,138),
        ("Start Download",self.start_download_thread,150),
        ("Pause",None,82),
        ("Resume",None,88)
    ]:
        ctk.CTkButton(
            left_toolbar,
            text=txt,
            width=w,
            height=34,
            corner_radius=8,
            command=cmd
        ).pack(side="left", padx=4)


    right_toolbar=ctk.CTkFrame(top, fg_color=BG)
    right_toolbar.grid(
        row=0,
        column=1,
        sticky="e",
        padx=8
    )

    # try:
    #     self.banner_img=ctk.CTkImage(
    #         light_image=Image.open(
    #             "assets/top_network_banner.png"
    #         ),
    #         size=(190,46)
    #     )

    #     ctk.CTkLabel(
    #         right_toolbar,
    #         image=self.banner_img,
    #         text=""
    #     ).pack(side="left",padx=8)

    # except:
    #     pass


    status_box=ctk.CTkFrame(
        right_toolbar,
        fg_color=PANEL,
        border_width=1,
        border_color=BORDER,
        corner_radius=8,
        width=145,
        height=44
    )
    status_box.pack(side="left")
    status_box.pack_propagate(False)

    self.conn_label=ctk.CTkLabel(
        status_box,
        text="Connected\nDHT Enabled",
        font=("Segoe UI",11,"bold")
    )
    self.conn_label.pack(expand=True)



    ##################################################
    # MAIN DASHBOARD
    ##################################################

    main=ctk.CTkFrame(
        self,
        fg_color=BG
    )
    main.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=6,
        pady=2
    )

    main.grid_columnconfigure(0,weight=24)
    main.grid_columnconfigure(1,weight=60)
    main.grid_columnconfigure(2,weight=16)
    main.grid_rowconfigure(0,weight=1)



    def section(parent):
        return ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )


    ##################################################
    # LEFT
    ##################################################

    left=section(main)
    left.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0,4)
    )

    left.grid_columnconfigure(0, weight=1)
    left.grid_columnconfigure(1, weight=0)

    ctk.CTkLabel(
        left,
        text="Torrent Information",
        font=("Segoe UI",17,"bold")
    ).pack(anchor="w",padx=12,pady=(10,4))

    self.meta_label = ctk.CTkLabel(
        left,
        text="Load torrent...",
        justify="left",
        anchor="w",
        font=("Consolas",12),
        wraplength=280   # adjust for your panel width
    )

    self.meta_label.pack(
        fill="x",
        padx=12,
        pady=2
    )
    self.stats_label=ctk.CTkLabel(
        left,
        text="",
        justify="left",
        anchor="w",
        font=("Consolas",12)
    )
    self.stats_label.pack(
        fill="x",
        padx=12,
        pady=5
    )

    ##################################################
    # CENTER
    ##################################################

    center=section(main)
    center.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=4
    )

    # center.grid_columnconfigure(0, weight=1) 
    # center.grid_columnconfigure(1, weight=0) 

    ctk.CTkLabel(
        center,
        text="Download Progress",
        font=("Segoe UI",17,"bold")
    ).pack(pady=(8,3))


    self.progressbar=ctk.CTkProgressBar(
        center,
        height=18
    )
    self.progressbar.pack(
        fill="x",
        padx=12,
        pady=4
    )
    self.progressbar.set(0)

    self.progress_label=ctk.CTkLabel(
        center,
        text="0%",
        font=("Segoe UI",12,"bold")
    )
    self.progress_label.pack(pady=(0,4))


    cards=ctk.CTkFrame(center,fg_color=PANEL)
    cards.pack(pady=6)


    def metric_card(txt):
        return ctk.CTkLabel(
            cards,
            text=txt,
            width=122,
            height=54,
            corner_radius=9,
            fg_color="white",
            font=("Segoe UI",11,"bold")
        )


    self.speed_card=metric_card("Speed\n0 MB/s")
    self.speed_card.pack(side="left",padx=3)

    self.timer_label=metric_card("Elapsed\n00:00")
    self.timer_label.pack(side="left",padx=3)

    self.remain_label=metric_card("Remaining\n--")
    self.remain_label.pack(side="left",padx=3)



    ctk.CTkLabel(
        center,
        text="Piece Map",
        font=("Segoe UI",15,"bold")
    ).pack(pady=(8,4))


    piece_wrap = ctk.CTkFrame(
        center,
        fg_color="white",
        border_width=1,
        border_color=BORDER,
        corner_radius=8
    )
    piece_wrap.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0,6)
    )


    self.piece_frame = ctk.CTkScrollableFrame(
        piece_wrap,
        fg_color="white",
        corner_radius=6
    )
    self.piece_frame.pack(
        fill="both",
        expand=True,
        padx=4,
        pady=4
    )

    ##################################################
    # RIGHT
    ##################################################

    right=section(main)
    right.grid(
        row=0,
        column=2,
        sticky="nsew",
        padx=(4,0)
    )

    ctk.CTkLabel(
        right,
        text="Peers (Connected)",
        font=("Segoe UI",17,"bold")
    ).pack(pady=(8,3))

    ctk.CTkLabel(
        right,
        text="IP Address             Status",
        font=("Consolas",11,"bold")
    ).pack()

    self.peer_box=ctk.CTkTextbox(
        right,
        font=("Consolas",11),
        corner_radius=8,
        border_width=1,
        border_color=BORDER
    )
    self.peer_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=6
    )



    ##################################################
    # BOTTOM
    ##################################################

    bottom=ctk.CTkFrame(
        self,
        fg_color=BG
    )
    bottom.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=6,
        pady=2
    )

    bottom.grid_columnconfigure(0,weight=80)
    bottom.grid_columnconfigure(1,weight=20)
    bottom.grid_rowconfigure(0,weight=1)



    log_frame=section(bottom)
    log_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0,4)
    )

    ctk.CTkLabel(
        log_frame,
        text="Activity Log",
        font=("Segoe UI",15,"bold")
    ).pack(pady=(6,3))

    self.logbox=ctk.CTkTextbox(
        log_frame,
        font=("Consolas",11),
        corner_radius=8,
        border_width=1,
        border_color=BORDER
    )
    self.logbox.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0,8)
    )



    ##################################################
    # IMPROVED SWARM OVERVIEW
    ##################################################

    swarm_frame=section(bottom)
    swarm_frame.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    ctk.CTkLabel(
        swarm_frame,
        text="Swarm Overview",
        font=("Segoe UI",15,"bold")
    ).pack(pady=(6,4))


    visual_panel=ctk.CTkFrame(
        swarm_frame,
        fg_color=PANEL,
        corner_radius=10
    )
    visual_panel.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0,8)
    )


    try:
        self.swarm_img=ctk.CTkImage(
            light_image=Image.open(
                "assets/swarm_overview.png"
            ),
            size=(344,224)
        )

        ctk.CTkLabel(
            visual_panel,
            image=self.swarm_img,
            text=""
        ).pack(
            expand=False,
            pady=8
        )

    except:
        ctk.CTkLabel(
            visual_panel,
            text="[swarm image]",
            text_color="white"
        ).pack(expand=True)



    ##################################################
    # FOOTER
    ##################################################

    footer=ctk.CTkFrame(
        self,
        height=28,
        fg_color=BG,
        border_width=1,
        border_color=BORDER,
        corner_radius=7
    )
    footer.grid(
        row=3,
        column=0,
        sticky="ew",
        padx=6,
        pady=(2,6)
    )
    footer.grid_propagate(False)


    self.status_label=ctk.CTkLabel(
        footer,
        text="Status: Idle",
        font=("Segoe UI",11)
    )
    self.status_label.pack(
        side="left",
        padx=12
    )
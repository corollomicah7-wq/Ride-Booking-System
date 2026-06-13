import tkinter as tk
from tkinter import ttk, messagebox

from vehicle import VEHICLES, VEHICLE_LABELS, KNOWN_LOCATIONS, calc_cost
from Booking import Booking
from booking_manager import BookingManager

# Palette 
BG   = "#600404"; PANEL = "#7E0404"; INP = "#600404"
TEA  = "#DC6D06"; RED   = "#845B5B"; TXT = "#FFFFFF"; MUT = "#F08011"
RODD = "#E98E17"; REVEN = "#FFFFFF"; GOLD = "#E69317"

VEH_DISPLAY = list(VEHICLE_LABELS.keys())
DEFAULT_VEH = "Choose Vehicle"

class RideBookingApp:
    def __init__(self, root):
        self.root    = root
        self.manager = BookingManager("bookings.txt")
        self.next_id = self._calc_next_id()
        root.title("Ride Booking")
        root.configure(bg=BG)
        root.geometry("520x650")  # Default initial size
        root.resizable(False, False)
        self._setup_styles()
        
        # Base Application Frames
        self.welcome_frame = tk.Frame(self.root, bg=BG)
        self.main_app_frame = tk.Frame(self.root, bg=BG)
        self._container = tk.Frame(self.main_app_frame, bg=BG)
        
        # Create Widgets
        self.create_welcome_widgets()
        self.create_widgets()
        
        # Start at Homepage
        self.show_welcome_page()

    def _calc_next_id(self):
        ids = [int(b.booking_id) for b in self.manager.bookings if str(b.booking_id).isdigit()]
        return max(ids, default=0) + 1

    def _setup_styles(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("T.Treeview", background=RODD, foreground=TXT, rowheight=32,
                    fieldbackground=RODD, borderwidth=0, font=("Georgia", 9))
        s.configure("T.Treeview.Heading", background=INP, foreground=TEA,
                    relief="flat", font=("Georgia", 9, "bold"))
        s.map("T.Treeview", background=[("selected", "#1E3040")])
        s.configure("TCombobox", fieldbackground=TXT, background=INP,
            foreground="#000000", arrowcolor=TEA, selectbackground=TXT, selectforeground="#000000")
        s.map("TCombobox", fieldbackground=[("readonly", TXT)],
      selectbackground=[("readonly", TXT)], selectforeground=[("readonly", "#000000")])

    def _combo(self, parent, values, var):
        f = tk.Frame(parent, bg=TEA)
        tk.Frame(f, bg=TEA, width=3).pack(side="left", fill="y")
        cb = ttk.Combobox(f, textvariable=var, values=values, state="readonly", font=("Georgia", 10))
        cb.pack(side="left", fill="x", expand=True)
        f.pack(fill="x", padx=20); return cb

    def _btn(self, parent, text, cmd, bg=TEA, fg=BG, **kw):
        b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg, relief="flat",
                      font=("Georgia", 10, "bold"), cursor="hand2",
                      activebackground=bg, activeforeground=fg, bd=0, padx=14, pady=9, **kw)
        hov = "#00b89a" if bg == TEA else "#cc3d55" if bg == RED else "#1a3a4a" if bg == "#1E2D3D" else "#252D3D"
        b.bind("<Enter>", lambda e: b.config(bg=hov))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def _flabel(self, parent, text):
        tk.Label(parent, text=text, bg=PANEL, fg="#FFFFFF",
                 font=("Georgia", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(8,2))

    # Welcome Widgets
    def create_welcome_widgets(self):
        center_panel = tk.Frame(self.welcome_frame, bg=PANEL, padx=40, pady=50)
        center_panel.place(relx=0.5, rely=0.5, anchor="center")
        
        title_frame = tk.Frame(center_panel, bg=PANEL)
        title_frame.pack(pady=(0, 20))
        
        tk.Label(title_frame, text="Ride Booking", bg=PANEL, fg=TEA, font=("Georgia", 36, "bold")).pack(side="top")
        
        tk.Label(center_panel, text="Book your ride Now!", 
                 bg=PANEL, fg=MUT, font=("Georgia", 11)).pack(pady=(0, 40))
        
        self._btn(center_panel, "BOOK NOW →", self.show_main_system, bg=TEA, fg=BG).pack(ipadx=20, ipady=4)

    # Widgets Setup for Main App
    def create_widgets(self):
        # Header 
        h = tk.Frame(self.main_app_frame, bg=BG, height=56); h.pack(fill="x"); h.pack_propagate(False)
        self._btn(h, "← BACK", self.show_welcome_page, bg=INP, fg=MUT).pack(side="left", padx=15, pady=12)
        tk.Label(h, text="Ride Booking", bg=BG, fg=TXT, font=("Georgia", 18, "bold")).pack(side="left", padx=(14,0), pady=12)
        tk.Frame(self.main_app_frame, bg="#6C0404", height=1).pack(fill="x")

        self._btn(h, "👥 PORTFOLIO", self.show_portfolio, bg=INP, fg=TEA).pack(side="right", padx=15, pady=12)
       

        self._container.pack(fill="both", expand=True)

        self._build_portfolio_page()
        self._build_form_page()
        self._build_records_page()
        self._form_page.pack(fill="both", expand=True)

    # Form page 
    def _build_form_page(self):
        self._form_page = tk.Frame(self._container, bg=BG)

        card = tk.Frame(self._form_page, bg=PANEL)
        card.pack(fill="x", padx=24, pady=(16, 8))

        tk.Frame(card, bg=TEA, width=4, height=20).place(x=18, y=18)
        tk.Label(card, text="  NEW BOOKING", bg=PANEL, fg=TXT,
                 font=("Georgia", 11, "bold")).pack(anchor="w", padx=18, pady=(18,4))
        tk.Frame(card, bg="#6C0404", height=1).pack(fill="x", padx=18, pady=(0,4))

        self._flabel(card, "PASSENGER NAME")
        nf = tk.Frame(card, bg=TXT); tk.Frame(nf, bg=TXT, width=3).pack(side="left", fill="y")
        self._e_name = tk.Entry(nf, bg=TXT, fg="#000000", relief="flat",
                        font=("Georgia", 10), insertbackground="#000000", bd=6)
        self._e_name.pack(side="left", fill="both", expand=True)
        nf.pack(fill="x", padx=20)

        self._flabel(card, "START LOCATION")
        self._start_var = tk.StringVar(value="")
        self._combo(card, KNOWN_LOCATIONS, self._start_var)

        self._flabel(card, "END LOCATION")
        self._end_var = tk.StringVar(value="")
        self._combo(card, KNOWN_LOCATIONS, self._end_var)

        self._flabel(card, "VEHICLE TYPE")
        self._veh = tk.StringVar(value="")
        veh_combo = self._combo(card, VEH_DISPLAY, self._veh)
        veh_combo.bind("<<ComboboxSelected>>", self._on_vehicle_change)

        # Vehicle info panel
        self._veh_info = tk.Frame(card, bg="#FFFFFF", padx=12, pady=8)
        
        self._veh_emoji_lbl = tk.Label(self._veh_info, text="", bg="#FFFFFF", fg="#000000", font=("Georgia", 20))
        self._veh_emoji_lbl.pack(side="left", padx=(0, 10))
        
        veh_details = tk.Frame(self._veh_info, bg="#FFFFFF")
        veh_details.pack(side="left", fill="x", expand=True)
        
        # Vehicle name
        self._veh_name_lbl = tk.Label(veh_details, text="", bg="#FFFFFF", fg="#000000", font=("Georgia", 10, "bold"), anchor="w")
        self._veh_name_lbl.pack(fill="x")
        
        # Capacity dropdown setup
        cap_frame = tk.Frame(veh_details, bg="#FFFFFF")
        cap_frame.pack(fill="x")
        
        # Capacity label
        tk.Label(cap_frame, text="👤 Capacity: ", bg="#FFFFFF", fg=GOLD, font=("Georgia", 9)).pack(side="left")
        
        # Capacity dropdown
        self._capacity_var = tk.StringVar()
        self._capacity_combo = ttk.Combobox(cap_frame, textvariable=self._capacity_var, state="readonly", width=6, font=("Georgia", 9))
        self._capacity_combo.pack(side="left", padx=5)
        
        self._veh_rate_lbl = tk.Label(veh_details, text="", bg="#FFFFFF", fg=TEA, font=("Georgia", 9), anchor="w")
        self._veh_rate_lbl.pack(fill="x")
        
        self._on_vehicle_change()
        
        self._divider = tk.Frame(card, bg="#252D3D", height=1)
        self._divider.pack(fill="x", padx=18, pady=10)

        tk.Frame(card, bg="#FFFFFF", height=1).pack(fill="x", padx=18, pady=10)
        self._btn(card, "✓  BOOK RIDE",  self.book_ride,    bg=TEA, fg=BG ).pack(fill="x", padx=20, pady=3)
        self._btn(card, "↺  CLEAR",      self.clear_inputs, bg=INP, fg=MUT).pack(fill="x", padx=20, pady=(3,14))

        # View records button
        self._btn(self._form_page, "☰  VIEW BOOKING RECORDS", self.show_records,
                  bg="#DC6D06", fg=BG).pack(fill="x", padx=24, pady=(4, 16))

    def _on_vehicle_change(self, event=None):
        label = self._veh.get()
        vtype = VEHICLE_LABELS.get(label)
        vobj  = VEHICLES.get(vtype) if vtype else None
        if not vobj:
            self._veh_info.pack_forget() 
            return
        
        if hasattr(self, '_divider'):
            self._veh_info.pack(fill="x", padx=20, pady=(4, 2), before=self._divider)
        else:
            self._veh_info.pack(fill="x", padx=20, pady=(4, 2))
        
        self._veh_info.pack(fill="x", padx=20, pady=(4, 2))
        
        options = vobj.get_capacity_options()
        self._veh_emoji_lbl.config(text=vobj._emoji)
        
        
        self._veh_name_lbl.config(text=vobj.get_type().upper())
        self._veh_rate_lbl.config(text=f"₱{vobj.get_base_fare():.0f} base  +  ₱{vobj.get_rate():.0f}/km")
        
        self._capacity_combo.config(values=options)
        if options:
            self._capacity_combo.current(0)

    # For Records page
    def _build_records_page(self):
        self._records_page = tk.Frame(self._container, bg=BG)

        tb = tk.Frame(self._records_page, bg=BG)
        tb.pack(fill="x", padx=18, pady=(14,6))
        tk.Label(tb, text="BOOKING RECORDS", bg=BG, fg=GOLD,
                 font=("Georgia", 11, "bold")).pack(side="left")
        self._cnt = tk.StringVar(value="0 bookings")
        tk.Label(tb, textvariable=self._cnt, bg=BG, fg=MUT, font=("Georgia", 9)).pack(side="left", padx=10)
        self._btn(tb, "⟳ REFRESH", self.refresh_table,  bg=PANEL, fg=TXT).pack(side="right", padx=(2,0))

        tf = tk.Frame(self._records_page, bg=BG)
        tf.pack(fill="both", expand=True, padx=18, pady=(0, 4))
        cols = ("id","user","vehicle","start","end","distance","cost")
        self._tree = ttk.Treeview(tf, columns=cols, show="headings",
                                  style="T.Treeview", selectmode="browse")
        for col, lbl, w in [("id","ID",45),("user","Passenger",120),("vehicle","Vehicle",110),
                             ("start","From",105),("end","To",105),("distance","km",55),("cost","₱ Cost",85)]:
            self._tree.heading(col, text=lbl)
            self._tree.column(col, width=w, anchor="center", minwidth=35)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        self._tree.bind("<Button-1>", self.cancel_booking) 
        
        self._tree.tag_configure("odd",  background=RODD)
        self._tree.tag_configure("even", background=RODD)

        # Back button bar 
        tk.Frame(self._records_page, bg="#FFFFFF", height=1).pack(fill="x")
        bot = tk.Frame(self._records_page, bg=PANEL)
        bot.pack(fill="x", side="bottom")
        self._btn(bot, "←  NEW BOOKING", self.show_booking_form,
                  bg=TEA, fg=BG).pack(side="left", padx=18, pady=12)
        
    def _build_portfolio_page(self):
        self._portfolio_page = tk.Frame(self._container, bg=BG)

        card = tk.Frame(self._portfolio_page, bg=PANEL)
        card.pack(fill="both", expand=True, padx=24, pady=16)

    # Header Title
        tk.Frame(card, bg=TEA, width=4, height=20).place(x=18, y=18)
        tk.Label(card, text="  GROUP PORTFOLIO", bg=PANEL, fg=TXT,
             font=("Georgia", 11, "bold")).pack(anchor="w", padx=18, pady=(18, 4))
        tk.Frame(card, bg="#252D3D", height=1).pack(fill="x", padx=18, pady=(0, 10))

        self._detail_box = tk.Frame(card, bg="#7E0404", padx=15, pady=12)
        self._detail_box.pack(side="bottom", fill="x", padx=18, pady=(5, 10))

        self._p_title = tk.Label(self._detail_box, text="💡 Click a member to view full profile",
                             bg="#7E0404", fg=GOLD, font=("Georgia", 10, "bold"), anchor="w")
        self._p_title.pack(fill="x", pady=(0, 4))

        self._p_info = tk.Label(self._detail_box, text="", bg="#7E0404", fg=TXT,
                            font=("Georgia", 9), anchor="w", justify="left")
        self._p_info.pack(fill="x")

    #Scrollbar
        wrapper = tk.Frame(card, bg=PANEL)
        wrapper.pack(fill="both", expand=True, padx=18, pady=(0, 6))

        canvas = tk.Canvas(wrapper, bg=PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=PANEL)
        inner_window = canvas.create_window((0, 0), window=inner, anchor="nw")

    # Canvas resizing
        def _on_canvas_resize(event):
            canvas.itemconfig(inner_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_resize)

        inner.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    # Mouse-wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind only when mouse is over the canvas area
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    

    # Member data
        members = [
            {
            "NAME": "Reian A. Fortunado",
            "ROLE": "OOP Developer/vehicle.py file",
            "SECTION": "BSCpE 1-5",
            "BIO": "1st-year Computer Engineering student who chose this program and doesn't want to be anywhere else but here."
            },
            {
            "NAME": "Gwynn O. Magpantay",
            "ROLE": "OOP Developer/Booking.py file",
            "SECTION": "BSCpE 1-5",
            "BIO": "Babay Comp eng hello HM"
            },
            {
            "NAME": "Karl Abijah F. Morato",
            "ROLE": "OOP Developer/Booking_manager.py file",
            "SECTION": "BSCpE 1-5",
            "BIO": "CTRL-Z is life"
            },
            {
            "NAME": "Denver James P. Quizan",
            "ROLE": "OOP Developer/gui.py file",
            "SECTION": "BSCpE 1-5",
            "BIO": "Don't give up on your dreams keep sleeping."
            },
            {
            "NAME": "Kirby Renzo F. Jardio",
            "ROLE": "Developer",
            "SECTION": "BSCpE 1-5",
            "BIO": "Sacrifice the pawn to control the board"
            },
            {
            "NAME": "Micah L. Corollo",
            "ROLE": "OOP Testing/Adjusting",
            "SECTION": "BSCpE 1-5",
            "BIO": "See u in 2nd Yr"
            },
            {
            "NAME": "",
            "ROLE": "",
            "SECTION": "BSCpE 1-5",
            "BIO": "dfrfr"
            },
            {
            "NAME": "Venice Andrei P. Mose",
            "ROLE": "Research Writer / Introduction",
            "SECTION": "BSCpE 1-5",
            "BIO": "Proverbs 3:5"
            },
            {
            "NAME": "Princess Aleeya T. Madamba",
            "ROLE": "Research Writer / Testing & Result",
            "SECTION": "BSCPE 1-5",
            "BIO": "ad meliora"
            }
            
        ]

        def on_member_select(member_data):
            self._p_title.config(text=f"👤 {member_data['NAME'].upper()} — {member_data['ROLE']}")
            self._p_info.config(text=f"{member_data['SECTION']}\n\n{member_data['BIO']}")

    # Build member cards inside 'inner' scrollable
        for m in members:
            m_frame = tk.Frame(inner, bg=INP, padx=15, pady=8, cursor="hand2")
            m_frame.pack(fill="x", pady=4)

            lbl_NAME = tk.Label(m_frame, text=m["NAME"], bg=INP, fg=TXT,
                            font=("Georgia", 10, "bold"), anchor="w", cursor="hand2")
            lbl_NAME.pack(fill="x")

            lbl_ROLE = tk.Label(m_frame, text=m["ROLE"], bg=INP, fg=TEA,
                            font=("Georgia", 8), anchor="w", cursor="hand2")
            lbl_ROLE.pack(fill="x")

        # Click to view profile
            for widget in (m_frame, lbl_NAME, lbl_ROLE):
                widget.bind("<Button-1>", lambda e, data=m: on_member_select(data))
        
            def on_enter(e, f=m_frame, n=lbl_NAME, r=lbl_ROLE):
                f.config(bg="#252D3D"); n.config(bg="#252D3D"); r.config(bg="#252D3D")
            def on_leave(e, f=m_frame, n=lbl_NAME, r=lbl_ROLE):
                f.config(bg=INP); n.config(bg=INP); r.config(bg=INP)

            for widget in (m_frame, lbl_NAME, lbl_ROLE):
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)


        # Bottom navigation elements
        tk.Frame(card, bg="#252D3D", height=1).pack(fill="x", side="bottom", padx=18, pady=(0, 10))
        self._btn(card, "←  BACK TO BOOKING", self.show_booking_form, bg=TEA, fg=BG).pack(fill="x", side="bottom", padx=20, pady=(0, 2))

    # Page switching 
    def show_welcome_page(self):
        self.main_app_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)
        self.root.geometry("520x650")

    def show_main_system(self):
        self.welcome_frame.pack_forget()
        self.main_app_frame.pack(fill="both", expand=True)
        self.show_booking_form()

    def show_portfolio(self):
        self._form_page.pack_forget()
        self._records_page.pack_forget()
        self._portfolio_page.pack(fill="both", expand=True)
        if hasattr(self, '_status_bar'):
            self._status_bar.pack_forget()
            self._status_bar.pack(side="bottom", fill="x")
        self.root.geometry("520x650")
        
    def show_booking_form(self):
        self._portfolio_page.pack_forget()
        if hasattr(self, '_records_page'): 
            self._records_page.pack_forget()
            self._form_page.pack(fill="both", expand=True)
        self.root.geometry("520x650")

    def show_records(self):
        self._form_page.pack_forget()
        self.refresh_table()
        self._records_page.pack(fill="both", expand=True)
        self.root.geometry("650x650")

    # Methods 
    def book_ride(self):
        name  = self._e_name.get().strip()
        start = self._start_var.get().strip()
        end   = self._end_var.get().strip()
        label = self._veh.get()
        vtype = VEHICLE_LABELS.get(label)
        seat  = self._capacity_var.get()

        if not all([name, start, end]):
            messagebox.showerror("Error", "There's no Input.", parent=self.root); return
        if start.lower() == end.lower():
            messagebox.showerror("Error", "Start and End must differ.", parent=self.root); return
        if not vtype:
            messagebox.showerror("Error", "Please select a vehicle.", parent=self.root); return

        dist, cost = calc_cost(start, end, vtype)
        bid = self.get_next_booking_id()
        self.manager.add_booking(Booking(bid, name, vtype, start, end, dist))
        self.clear_inputs()
        
        self.show_records()

    def cancel_booking(self, event):
        selected_item = self._tree.identify_row(event.y)
        if not selected_item:
             return
         
        self._tree.selection_set(selected_item)
         
        row_values = self._tree.item(selected_item, "values")
        booking_id = int(row_values[0])
        
        confirmed = messagebox.askyesno(
            title="Cancel Booking",
            message=f"Are you sure you want to cancel Booking #{booking_id}?"
        )
        if confirmed:
            self.manager.bookings = [b for b in self.manager.bookings if str(b.booking_id) != str(booking_id)]
            if hasattr(self.manager, 'save_bookings'):
                self.manager.save_bookings()
            elif hasattr(self.manager, 'save_to_file'):
                self.manager.save_to_file()
                
        else:
            pass
        self.refresh_table()
        
    def refresh_table(self):
        for i in self._tree.get_children(): self._tree.delete(i)
        for i, b in enumerate(self.manager.bookings):
            lbl = b.vehicle.get_label() if b.vehicle else b.vehicle_type
            self._tree.insert("", "end",
                values=(b.booking_id, b.user, lbl, b.start_location, b.end_location,
                        f"{b.distance:.1f}", f"{b.total_cost:,.2f}"),
                tags=("odd" if i % 2 == 0 else "even",))
        n = len(self.manager.bookings)
        self._cnt.set(f"{n} booking{'s' if n != 1 else ''}")

    def clear_inputs(self):
        self._e_name.delete(0, "end")
        self._start_var.set(""); self._end_var.set("")
        self._veh.set(DEFAULT_VEH)
        self._on_vehicle_change()

    def get_next_booking_id(self):
        bid = self.next_id; self.next_id +=     1; return bid


if __name__ == "__main__":
    root = tk.Tk()
    RideBookingApp(root)
    root.mainloop()

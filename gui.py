import tkinter as tk
from tkinter import ttk, messagebox

from vehicle import VEHICLE_LABELS, KNOWN_LOCATIONS, calc_cost
from booking import Booking
from booking_manager import BookingManager

# Palette
BG   = "#0D0F14"; PANEL = "#161B24"; INP = "#1E2533"
TEA  = "#00E5C3"; RED   = "#FF4D6A"; TXT = "#E8ECF2"; MUT = "#6B7A99"
RODD = "#161B24"; REVEN = "#1A2030"

VEH_DISPLAY = list(VEHICLE_LABELS.keys())
DEFAULT_VEH = VEH_DISPLAY[0]

# App 
class RideBookingApp:
    def __init__(self, root):
        self.root    = root
        self.manager = BookingManager("bookings.txt")
        self.next_id = self._calc_next_id()
        root.title("Ride — Booking System")
        root.configure(bg=BG)
        root.geometry("1000x650")
        self._setup_styles()
        self.create_widgets()
        self.refresh_table()

    def _calc_next_id(self):
        ids = [int(b.booking_id) for b in self.manager.bookings if str(b.booking_id).isdigit()]
        return max(ids, default=0) + 1

    def _setup_styles(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("T.Treeview", background=RODD, foreground=TXT, rowheight=32,
                    fieldbackground=RODD, borderwidth=0, font=("Segoe UI", 9))
        s.configure("T.Treeview.Heading", background=INP, foreground=TEA,
                    relief="flat", font=("Segoe UI", 9, "bold"))
        s.map("T.Treeview", background=[("selected", "#1E3040")])
        s.configure("TCombobox", fieldbackground=INP, background=INP,
                    foreground=TXT, arrowcolor=TEA, selectbackground=INP, selectforeground=TXT)
        s.map("TCombobox", fieldbackground=[("readonly", INP)],
              selectbackground=[("readonly", INP)], selectforeground=[("readonly", TXT)])

    def _combo(self, parent, values, textvariable):
        """Styled combobox with teal left-bar."""
        f = tk.Frame(parent, bg=TEA)
        tk.Frame(f, bg=TEA, width=3).pack(side="left", fill="y")
        cb = ttk.Combobox(f, textvariable=textvariable, values=values,
                          state="readonly", font=("Segoe UI", 10))
        cb.pack(side="left", fill="x", expand=True)
        f.pack(fill="x"); return cb

    def _btn(self, parent, text, cmd, bg=TEA, fg=BG, **kw):
        b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg, relief="flat",
                      font=("Segoe UI", 10, "bold"), cursor="hand2",
                      activebackground=bg, activeforeground=fg, bd=0, padx=14, pady=8, **kw)
        hov = "#00b89a" if bg == TEA else "#cc3d55" if bg == RED else "#252D3D"
        b.bind("<Enter>", lambda e: b.config(bg=hov))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    # create_widgets 
    def create_widgets(self):
        # Header
        h = tk.Frame(self.root, bg=BG, height=56); h.pack(fill="x"); h.pack_propagate(False)
        tk.Label(h, text="RIDE", bg=BG, fg=TXT, font=("Segoe UI", 18, "bold")).pack(side="left", padx=(24,0), pady=12)
        tk.Label(h, text="  Booking System", bg=BG, fg=MUT, font=("Segoe UI", 16, "bold")).pack(side="left", pady=14)
        tk.Frame(self.root, bg="#252D3D", height=1).pack(fill="x")

        body = tk.Frame(self.root, bg=BG); body.pack(fill="both", expand=True, padx=18, pady=14)

        # Left panel
        left = tk.Frame(body, bg=PANEL, width=290); left.pack(side="left", fill="y", padx=(0,14)); left.pack_propagate(False)
        tk.Frame(left, bg=TEA, width=4, height=20).place(x=18, y=22)
        tk.Label(left, text="  NEW BOOKING", bg=PANEL, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(18,4))
        tk.Frame(left, bg="#252D3D", height=1).pack(fill="x", padx=18, pady=(0,10))

        # Name entry
        tk.Label(left, text="PASSENGER NAME", bg=PANEL, fg=MUT, font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(6,2))
        nf = tk.Frame(left, bg=TEA); tk.Frame(nf, bg=TEA, width=3).pack(side="left", fill="y")
        self._e_name = tk.Entry(nf, bg=INP, fg=TXT, relief="flat", font=("Segoe UI", 10), insertbackground=TEA, bd=6)
        self._e_name.pack(side="left", fill="both", expand=True); nf.pack(fill="x", padx=20)

        # Start / End as dropdowns from KNOWN_LOCATIONS
        tk.Label(left, text="SELECT START LOCATION", bg=PANEL, fg=MUT, font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(6,2))
        self._start_var = tk.StringVar()
        self._combo(left, KNOWN_LOCATIONS, self._start_var)

        tk.Label(left, text="SELECT END LOCATION", bg=PANEL, fg=MUT, font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(6,2))
        self._end_var = tk.StringVar()
        self._combo(left, KNOWN_LOCATIONS, self._end_var)

        # Vehicle dropdown
        tk.Label(left, text="VEHICLE TYPE", bg=PANEL, fg=MUT, font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(6,2))
        self._veh = tk.StringVar(value="CHOOSE VEHICLE")
        self._combo(left, VEH_DISPLAY, self._veh)

        tk.Frame(left, bg="#252D3D", height=1).pack(fill="x", padx=18, pady=12)
        self._btn(left, "✓  BOOK RIDE",       self.book_ride,      bg=TEA, fg=BG).pack(fill="x", padx=20, pady=3)
        self._btn(left, "✕  CANCEL SELECTED",  self.cancel_booking, bg=RED, fg=TXT).pack(fill="x", padx=20, pady=3)
        self._btn(left, "↺  CLEAR",            self.clear_inputs,   bg=INP, fg=MUT).pack(fill="x", padx=20, pady=3)

        # Right panel
        right = tk.Frame(body, bg=BG); right.pack(side="left", fill="both", expand=True)
        th = tk.Frame(right, bg=BG); th.pack(fill="x", pady=(0,8))
        tk.Label(th, text="BOOKING RECORDS", bg=BG, fg=TXT, font=("Segoe UI", 11, "bold")).pack(side="left")
        self._cnt = tk.StringVar(value="0 bookings")
        tk.Label(th, textvariable=self._cnt, bg=BG, fg=MUT, font=("Segoe UI", 9)).pack(side="left", padx=10)
        self._btn(th, "⟳ REFRESH", self.refresh_table, bg=INP, fg=MUT).pack(side="right")

        tf = tk.Frame(right, bg=BG); tf.pack(fill="both", expand=True)
        cols = ("id","user","vehicle","start","end","distance","cost")
        self._tree = ttk.Treeview(tf, columns=cols, show="headings", style="T.Treeview", selectmode="browse")
        for col, lbl, w in [("id","ID",50),("user","Passenger",130),("vehicle","Vehicle",115),
                              ("start","From",110),("end","To",110),("distance","km",65),("cost","₱ Cost",90)]:
            self._tree.heading(col, text=lbl); self._tree.column(col, width=w, anchor="center", minwidth=40)
        sb = ttk.Scrollbar(tf, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        self._tree.tag_configure("odd", background=RODD); self._tree.tag_configure("even", background=REVEN)

        # Status bar
        tk.Frame(self.root, bg="#252D3D", height=1).pack(fill="x")
        sf = tk.Frame(self.root, bg=PANEL, height=28); sf.pack(fill="x"); sf.pack_propagate(False)
        self._status_var = tk.StringVar(value="Ready.")
        tk.Label(sf, textvariable=self._status_var, bg=PANEL, fg=MUT, font=("Segoe UI", 8), anchor="w").pack(side="left", padx=14)

    # Methods
    def book_ride(self):
        name  = self._e_name.get().strip()
        start = self._start_var.get().strip()
        end   = self._end_var.get().strip()
        label = self._veh.get()
        vtype = VEHICLE_LABELS.get(label)

        if not all([name, start, end]):
            messagebox.showerror("Error", "All fields are required.", parent=self.root); return
        if start.lower() == end.lower():
            messagebox.showerror("Error", "Start and End must differ.", parent=self.root); return
        if not vtype:
            messagebox.showerror("Error", "Please select a vehicle.", parent=self.root); return

        dist, cost = calc_cost(start, end, vtype)
        bid = self.get_next_booking_id()
        booking = Booking(bid, name, vtype, start, end, dist)
        self.manager.add_booking(booking)
        self.refresh_table()
        self.clear_inputs()
        self._status_var.set(f"✓ Booking #{bid} confirmed — {start} → {end}  ₱{cost:,.2f}")

    def cancel_booking(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select a row first.", parent=self.root); return
        bid = self._tree.set(sel[0], "id")
        rec = next((b for b in self.manager.bookings if str(b.booking_id) == str(bid)), None)
        if rec and messagebox.askyesno("Confirm", f"Cancel booking #{bid} for {rec.user}?", parent=self.root):
            self.manager.cancel_booking(bid)
            self.refresh_table()
            self._status_var.set(f"✗ Booking #{bid} cancelled.")

    def refresh_table(self):
        for i in self._tree.get_children(): self._tree.delete(i)
        for i, b in enumerate(self.manager.bookings):
            label = b.vehicle.get_label() if b.vehicle else b.vehicle_type
            self._tree.insert("", "end",
                values=(b.booking_id, b.user, label,
                        b.start_location, b.end_location,
                        f"{b.distance:.1f}", f"{b.total_cost:,.2f}"),
                tags=("odd" if i % 2 == 0 else "even",))
        n = len(self.manager.bookings)
        self._cnt.set(f"{n} booking{'s' if n != 1 else ''}")

    def clear_inputs(self):
        self._e_name.delete(0, "end")
        self._start_var.set(""); self._end_var.set("")
        self._veh.set(DEFAULT_VEH)

    def get_next_booking_id(self):
        bid = self.next_id; self.next_id += 1; return bid

if __name__ == "__main__":
    root = tk.Tk()
    RideBookingApp(root)
    root.mainloop()

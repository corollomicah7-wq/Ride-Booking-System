import tkinter as tk
from tkinter import ttk, messagebox


from vehicle import VEHICLES
from distance_service import distance_between_cities
# Palette 
BG   = "#0D0F14"; PANEL = "#161B24"; INP = "#1E2533"
TEA  = "#00E5C3"; RED   = "#FF4D6A"; TXT = "#E8ECF2"; MUT = "#6B7A99"
RODD = "#161B24"; REVEN = "#1A2030"


def calc_cost(start, end, vehicle_type):
    try:
        dist = distance_between_cities(start, end)
        if vehicle_type == "Car🚙":
            cost = 20 + (dist * 10)
        elif vehicle_type == "Van 🚐":
            cost = 50 + (dist * 15)
        elif vehicle_type == "Motorcycle 🏍":
            cost = dist * 5
        else:
            raise ValueError("Invalid vehicle type.")
        return dist, cost
    except Exception as e:
        print(f"Could not calculate distance/cost: {e}")
        return 0, 0
# App
class bookingapp:
    def __init__(self, root):
        self.root = root
        root.title("Ride — Booking System")
        root.configure(bg=BG)
        root.geometry("1000x650")
        self._setup_styles()
        self.create_widgets()
        self.next_id = 1
        self.bookings = []

    def _setup_styles(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("T.Treeview", background=RODD, foreground=TXT, rowheight=32,
                    fieldbackground=RODD, borderwidth=0, font=("Segoe UI", 9))
        s.configure("T.Treeview.Heading", background=INP, foreground=TEA,
                    relief="flat", font=("Segoe UI", 9, "bold"))
        s.map("T.Treeview", background=[("selected", "#1E3040")])
        s.configure("TCombobox", fieldbackground=INP, background=INP,
                    foreground=TXT, arrowcolor=TEA, selectbackground=INP,
                    selectforeground=TXT)
        s.map("TCombobox", fieldbackground=[("readonly", INP)],
              selectbackground=[("readonly", INP)], selectforeground=[("readonly", TXT)])

    def _label(self, p, t, fg=MUT, font=("Segoe UI", 8, "bold"), **kw):
        return tk.Label(p, text=t, bg=p["bg"] if hasattr(p, "__getitem__") else PANEL,
                        fg=fg, font=font, **kw)

    def _entry(self, p):
        f = tk.Frame(p, bg=TEA)
        tk.Frame(f, bg=TEA, width=3).pack(side="left", fill="y")
        e = tk.Entry(f, bg=INP, fg=TXT, relief="flat", font=("Segoe UI", 10),
                     insertbackground=TEA, bd=6)
        e.pack(side="left", fill="both", expand=True)
        f.pack(fill="x"); return e

    def _btn(self, p, text, cmd, bg=TEA, fg=BG, **kw):
        b = tk.Button(p, text=text, command=cmd, bg=bg, fg=fg, relief="flat",
                      font=("Segoe UI", 10, "bold"), cursor="hand2",
                      activebackground=bg, activeforeground=fg, bd=0,
                      padx=14, pady=8, **kw)
        b.bind("<Enter>", lambda e: b.config(bg="#00b89a" if bg == TEA else "#cc3d55" if bg == RED else "#252D3D"))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    # create_widgets 
    def create_widgets(self):
        # Header
        h = tk.Frame(self.root, bg=BG, height=56); h.pack(fill="x"); h.pack_propagate(False)
        tk.Label(h, text="RIDE", bg=BG, fg=TXT, font=("Segoe UI", 18, "bold")).pack(side="left", padx=(24,0), pady=12)
        tk.Label(h, text="  Booking System", bg=BG, fg=MUT, font=("Segoe UI", 10, "bold")).pack(side="left", pady=14)
        tk.Frame(self.root, bg="#252D3D", height=1).pack(fill="x")

        body = tk.Frame(self.root, bg=BG); body.pack(fill="both", expand=True, padx=18, pady=14)

        # Left form panel 
        left = tk.Frame(body, bg=PANEL, width=290); left.pack(side="left", fill="y", padx=(0,14)); left.pack_propagate(False)

        tk.Frame(left, bg=TEA, width=4, height=20).place(x=18, y=22)
        tk.Label(left, text="  NEW BOOKING", bg=PANEL, fg=TXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(18,4))
        tk.Frame(left, bg="#252D3D", height=1).pack(fill="x", padx=18, pady=(0,10))

        for lbl, attr in [("PASSENGER NAME", "_e_name"), ("START LOCATION", "_e_start"), ("END LOCATION", "_e_end")]:
            tk.Label(left, text=lbl, bg=PANEL, fg=MUT, font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(6,2))
            setattr(self, attr, self._entry(left))

        tk.Label(left, text="VEHICLE TYPE", bg=PANEL, fg=MUT, font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=20, pady=(6,2))
        vf = tk.Frame(left, bg=TEA); tk.Frame(vf, bg=TEA, width=3).pack(side="left", fill="y")
        self._veh = tk.StringVar(value="Choose Vehicles")
        ttk.Combobox(vf, textvariable=self._veh, values=list(VEHICLES), state="readonly",
                     font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True)
        vf.pack(fill="x", padx=20)

        tk.Frame(left, bg="#252D3D", height=1).pack(fill="x", padx=18, pady=12)

        self._btn(left, "✓  BOOK RIDE",       self.book_ride,      bg=TEA, fg=BG).pack(fill="x", padx=20, pady=3)
        self._btn(left, "✕  CANCEL SELECTED",  self.cancel_booking, bg=RED, fg=TXT).pack(fill="x", padx=20, pady=3)
        self._btn(left, "↺  CLEAR",            self.clear_inputs,   bg=INP, fg=MUT).pack(fill="x", padx=20, pady=3)

        # Right table panel 
        right = tk.Frame(body, bg=BG); right.pack(side="left", fill="both", expand=True)

        th = tk.Frame(right, bg=BG); th.pack(fill="x", pady=(0,8))
        tk.Label(th, text="BOOKING RECORDS", bg=BG, fg=TXT, font=("Segoe UI", 11, "bold")).pack(side="left")
        self._cnt = tk.StringVar(value="0 bookings")
        tk.Label(th, textvariable=self._cnt, bg=BG, fg=MUT, font=("Segoe UI", 9)).pack(side="left", padx=10)
        self._btn(th, "⟳ REFRESH", self.refresh_table, bg=INP, fg=MUT).pack(side="right", pady=0)

        tf = tk.Frame(right, bg=BG); tf.pack(fill="both", expand=True)
        cols = ("id","user","vehicle","start","end","distance","cost")
        self._tree = ttk.Treeview(tf, columns=cols, show="headings", style="T.Treeview", selectmode="browse")
        for col, lbl, w, anc in [("id","ID",50,"center"),("user","Passenger",130,"center"),
                                   ("vehicle","Vehicle",115,"center"),("start","From",110,"center"),
                                   ("end","To",110,"center"),("distance","km",65,"center"),("cost","₱ Cost",90,"center")]:
            self._tree.heading(col, text=lbl); self._tree.column(col, width=w, anchor=anc, minwidth=40)
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
        name, start, end = self._e_name.get().strip(), self._e_start.get().strip(), self._e_end.get().strip()
        if not all([name, start, end]):
            messagebox.showerror("Error", "All fields are required.", parent=self.root); return
        if start.lower() == end.lower():
            messagebox.showerror("Error", "Start and End must differ.", parent=self.root); return
        dist, cost = calc_cost(start, end, self._veh.get())
        b = {"id": self.get_next_booking_id(), "user": name, "vehicle": self._veh.get(),
             "start": start, "end": end, "distance": dist, "cost": cost}
        self.bookings.append(b); self.refresh_table(); self.clear_inputs()
        self._status_var.set(f"✓ Booking #{b['id']} confirmed — {start} → {end}  ₱{cost:,.2f}")

    def cancel_booking(self):
        sel = self._tree.selection()
        if not sel: messagebox.showinfo("Info", "Select a row first.", parent=self.root); return
        bid = int(self._tree.set(sel[0], "id"))
        rec = next((b for b in self.bookings if b["id"] == bid), None)
        if rec and messagebox.askyesno("Confirm", f"Cancel booking #{bid} for {rec['user']}?", parent=self.root):
            self.bookings.remove(rec); self.refresh_table()
            self._status_var.set(f"✗ Booking #{bid} cancelled.")

    def refresh_table(self):
        for i in self._tree.get_children(): self._tree.delete(i)
        for i, b in enumerate(self.bookings):
            self._tree.insert("", "end", values=(b["id"], b["user"], b["vehicle"],
                              b["start"], b["end"], f"{b['distance']:.1f}", f"{b['cost']:,.2f}"),
                              tags=("odd" if i % 2 == 0 else "even",))
        n = len(self.bookings); self._cnt.set(f"{n} booking{'s' if n != 1 else ''}")

    def clear_inputs(self):
        for e in (self._e_name, self._e_start, self._e_end): e.delete(0, "end")
        self._veh.set("Choose Vehicle")

    def get_next_booking_id(self):
        bid = self.next_id; self.next_id += 1; return bid



if __name__ == "__main__":
    root = tk.Tk()
    bookingapp(root)
    root.mainloop()

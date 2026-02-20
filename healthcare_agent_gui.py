
import os
import threading
import math
import time
import json
from datetime import datetime
from pathlib import Path
import textwrap
from dotenv import load_dotenv


# GUI
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog

# LLM / CrewAI - keep your integration intact
from crewai import Agent, Task, Crew, LLM

# Imaging
from PIL import Image, ImageDraw, ImageTk, ImageFilter

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdfcanvas

# Load env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------------------
# Theme presets (you can edit)
# ---------------------------
THEMES = {
    "Classic Ayurveda": {
        "bg": "#f5f3e7",
        "card": "#ffffff",
        "primary": "#4A6741",
        "accent": "#D4A373",
        "text": "#2b2b2b"
    },
    "Lotus Pink": {
        "bg": "#fff7fb",
        "card": "#ffffff",
        "primary": "#d86fa6",
        "accent": "#f7c6d7",
        "text": "#382033"
    },
    "Mystic Indigo": {
        "bg": "#0f1026",
        "card": "#131428",
        "primary": "#6a5acd",
        "accent": "#9aa0ff",
        "text": "#e8e9ff"
    },
    "Night Aura": {
        "bg": "#0b1220",
        "card": "#0f1724",
        "primary": "#00d2ff",
        "accent": "#8af6ff",
        "text": "#d9f7ff"
    }
}
CURRENT_THEME = THEMES["Classic Ayurveda"]

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

HISTORY_FILE = Path("consult_history.json")


# ---------------------------
# Utilities: image / logo / gradient
# ---------------------------
def make_gradient_image(size, color1, color2, horizontal=False):
    w, h = size
    base = Image.new("RGB", (w, h), color1)
    top = Image.new("RGB", (w, h), color2)
    mask = Image.new("L", (w, h))
    mask_data = []
    for y in range(h):
        for x in range(w):
            t = x / (w - 1) if horizontal else y / (h - 1)
            mask_data.append(int(255 * t))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def make_lotus_logo(size=(110,110)):
    """Create a layered lotus-like logo (PIL Image) suitable for rotation animation."""
    w, h = size
    cx, cy = w//2, h//2
    r = min(w,h)//3
    img = Image.new("RGBA", (w,h), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    # Glow background
    glow = Image.new("RGBA", (w,h), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(10):
        alpha = max(0, 28 - i*2)
        bbox = (cx-r-i, cy-r-i, cx+r+i, cy+r+i)
        gdraw.ellipse(bbox, fill=(76,103,65,alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, glow)

    # layered petals
    petal_colors = ["#ffd6a5", "#ffc4a3", "#f4a261", "#e76f51"]
    for layer in range(4):
        col = petal_colors[layer % len(petal_colors)]
        scale = 1.0 - layer*0.12
        for i in range(6):
            angle = math.radians(i*60 - 90)
            px = cx + math.cos(angle) * r * 0.08
            py = cy + math.sin(angle) * r * 0.08
            bbox = [
                px - r*scale, py - r*scale*0.6,
                px + r*scale, py + r*scale*1.2
            ]
            draw.ellipse(bbox, fill=col + "ff" if len(col)==7 else col)
    draw.ellipse((cx- r*0.28, cy - r*0.28, cx + r*0.28, cy + r*0.28), fill="#90BE6D")
    return img

def make_chakra_image(size=64):
    base = Image.new("RGBA", (size,size), (0,0,0,0))
    draw = ImageDraw.Draw(base)
    cx, cy = size//2, size//2
    r = int(size*0.35)
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(76,103,65,255), width=4)
    for i in range(6):
        ang = math.radians(i*60)
        x = cx + math.cos(ang) * r
        y = cy + math.sin(ang) * r
        draw.line((cx,cy,x,y), fill=(76,103,65,220), width=3)
    return base

# ---------------------------
# PDF export
# ---------------------------
def textwrap_lines(txt: str, width: int):
    return textwrap.wrap(txt, width=width) or [""]

def save_pdf_report(filepath: str, title: str, specialist: str, query: str, result_text: str):
    c = pdfcanvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor(CURRENT_THEME["primary"]))
    c.drawString(margin, y, "🌿 " + title)
    y -= 30

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(margin, y, f"Specialist: {specialist}    Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 18

    c.setStrokeColor(colors.HexColor(CURRENT_THEME["accent"]))
    c.line(margin, y, width - margin, y)
    y -= 14

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Patient Query:")
    y -= 14
    c.setFont("Helvetica", 10)
    t = c.beginText(margin, y)
    t.setLeading(14)
    for ln in textwrap_lines(query, 90):
        t.textLine(ln)
    c.drawText(t)
    y = t.getY() - 12

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Consultation Result:")
    y -= 14
    c.setFont("Helvetica", 10)
    t = c.beginText(margin, y)
    t.setLeading(14)
    for ln in textwrap_lines(result_text, 90):
        t.textLine(ln)
    c.drawText(t)
    c.showPage()
    c.save()

# ---------------------------
# History helpers (local JSON)
# ---------------------------
def load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def append_history(entry: dict):
    history = load_history()
    history.insert(0, entry)  # newest first
    # keep last 200
    history = history[:200]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# ---------------------------
# Main App class
# ---------------------------
class AyurvedaUltraX10000(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🌿 AI Ayurveda Assistant ")
        # Start maximized for best experience (keeps title bar)
        self.state("zoomed")
        self.minsize(1000, 720)

        # theme
        self.active_theme = tk.StringVar(value="Classic Ayurveda")
        self.apply_theme("Classic Ayurveda")

        # layout grid (2 columns: sidebar + main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # UI elements
        self.logo_img = make_lotus_logo((110,110))
        self.logo_angle = 0
        self.chakra_img = make_chakra_image(64)
        self.chakra_angle = 0

        self.is_processing = False
        self.last_result = ""
        self.last_specialist = ""
        self.last_query = ""

        # build
        self.create_header()
        self.create_sidebar(collapsed=False)
        self.create_main()

        # start logo rotation
        self._rotate_logo()

    # Theme apply
    def apply_theme(self, theme_name):
        global CURRENT_THEME
        CURRENT_THEME = THEMES.get(theme_name, THEMES["Classic Ayurveda"])
        self.configure(fg_color=CURRENT_THEME["bg"])
        if theme_name in ["Mystic Indigo", "Night Aura"]:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    # ---------------------------
    # Header: logo + title + theme menu + sidebar toggle
    # ---------------------------
    def create_header(self):
        header = ctk.CTkFrame(self, height=100, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=16, pady=(8,8))
        header.grid_columnconfigure(1, weight=1)

        # logo label (tk label to show rotated PIL image)
        self.logo_tk = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = tk.Label(header, image=self.logo_tk, bd=0, bg=CURRENT_THEME["bg"])
        self.logo_label.grid(row=0, column=0, padx=(8,12), sticky="w")

        title = ctk.CTkLabel(header, text="🌿 AI Ayurveda Assistant", font=ctk.CTkFont(size=40, weight="bold"))
        title.grid(row=0, column=1, sticky="w")

        # theme menu
        theme_menu = ctk.CTkOptionMenu(header, values=list(THEMES.keys()), command=self._on_theme_change)
        theme_menu.set("Classic Ayurveda")
        theme_menu.grid(row=0, column=2, sticky="e", padx=8)

        # sidebar toggle
        self.sidebar_collapsed = False
        toggle_btn = ctk.CTkButton(header, text="☰", width=40, command=self._toggle_sidebar)
        toggle_btn.grid(row=0, column=3, padx=(8,16), sticky="e")

    def _on_theme_change(self, val):
        self.active_theme.set(val)
        self.apply_theme(val)
        # refresh some widget colors manually if needed
        try:
            self.start_btn.configure(fg_color=CURRENT_THEME["primary"])
            self.clear_btn.configure(fg_color=CURRENT_THEME["accent"])
        except Exception:
            pass
        self.logo_label.configure(bg=CURRENT_THEME["bg"])

    def _rotate_logo(self):
        # smooth rotation for the logo
        self.logo_angle = (self.logo_angle + 2) % 360
        rotated = self.logo_img.rotate(self.logo_angle, resample=Image.BICUBIC)
        self.logo_tk = ImageTk.PhotoImage(rotated)
        self.logo_label.configure(image=self.logo_tk)
        self.logo_label.image = self.logo_tk
        self.after(50, self._rotate_logo)  # 20 fps approx

    # ---------------------------
    # Sidebar: animated collapse/expand
    # ---------------------------
    def create_sidebar(self, collapsed=False):
        # If there's existing sidebar, destroy it
        if hasattr(self, "sidebar_frame"):
            self.sidebar_frame.destroy()

        self.sidebar_frame = ctk.CTkFrame(self, width=320, corner_radius=8)
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=(16,8), pady=12)
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="🔮 Specialist", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=12, pady=(8,6), sticky="w")
        self.specialists = [
            "🧬 Prakriti & Dosha Analyst",
            "🧘 Ayurvedic Lifestyle Advisor",
            "🌿 Herbal & Remedy Guide",
            "🍃 Ahara (Diet) Specialist",
            "🕉 Yoga & Pranayama Guide",
            "🔥 Agni & Ama Consultant"
        ]
        self.role_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=self.specialists)
        self.role_menu.grid(row=1, column=0, padx=12, pady=(0,12), sticky="ew")
        self.role_menu.set(self.specialists[0])

        # action buttons & gradient simulation
        self.start_btn = ctk.CTkButton(self.sidebar_frame, text="✨ Start Consultation", height=48, fg_color=CURRENT_THEME["primary"], command=self.start_consultation_thread)
        self.start_btn.grid(row=2, column=0, padx=12, pady=(6,8), sticky="ew")
        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="🧹 Clear Output", height=40, fg_color=CURRENT_THEME["accent"], command=self.clear_output)
        self.clear_btn.grid(row=3, column=0, padx=12, pady=(0,8), sticky="ew")
        self.pdf_btn = ctk.CTkButton(self.sidebar_frame, text="📜 Download PDF Report", height=40, command=self._on_pdf_export)
        self.pdf_btn.grid(row=4, column=0, padx=12, pady=(6,8), sticky="ew")

        # spacer
        ctk.CTkLabel(self.sidebar_frame, text="").grid(row=5, column=0, pady=6)

        # history quick access
        self.history_quick_btn = ctk.CTkButton(self.sidebar_frame, text="🕘 View History", height=36, command=lambda: self.tabview.set("History"))
        self.history_quick_btn.grid(row=6, column=0, padx=12, pady=(6,6), sticky="ew")

        # disclaimer
        ctk.CTkLabel(self.sidebar_frame, text="⚠️ Educational Ayurvedic guidance only.", text_color="gray", wraplength=260).grid(row=8, column=0, padx=12, pady=(6,12))

    def _toggle_sidebar(self):
        # animated width change
        if self.sidebar_collapsed:
            # expand
            self._animate_sidebar(60, 320)
            self.sidebar_collapsed = False
        else:
            # collapse
            self._animate_sidebar(320, 60)
            self.sidebar_collapsed = True

    def _animate_sidebar(self, from_w, to_w, steps=10, delay=20):
        delta = (to_w - from_w) / steps
        def step(i=0, cur=from_w):
            w = int(from_w + delta * i)
            self.sidebar_frame.configure(width=w)
            if i < steps:
                self.after(delay, step, i+1, w)
            else:
                # final adjust
                self.sidebar_frame.configure(width=to_w)
        step()

    # ---------------------------
    # Main: Tabview with pages
    # ---------------------------
    def create_main(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=(8,16), pady=12)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Tabview
        self.tabview = ctk.CTkTabview(self.main_frame, width=900)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        # create tabs
        self.tabview.add("Consult")
        self.tabview.add("Diet Plan")
        self.tabview.add("Herbs")
        self.tabview.add("Yoga")
        self.tabview.add("Report")
        self.tabview.add("History")
        self.tabview.set("Consult")

        self._build_consult_tab()
        self._build_diet_tab()
        self._build_herbs_tab()
        self._build_yoga_tab()
        self._build_report_tab()
        self._build_history_tab()

    # ---------------------------
    # Consult tab contents
    # ---------------------------
    def _build_consult_tab(self):
        frame = self.tabview.tab("Consult")
        frame.grid_columnconfigure(1, weight=1)

        # left card: input
        input_card = ctk.CTkFrame(frame, corner_radius=12, fg_color=CURRENT_THEME["card"])
        input_card.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        ctk.CTkLabel(input_card, text="📝 Describe your symptoms & lifestyle", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(8,4))
        self.query_box = ctk.CTkTextbox(input_card, height=160, wrap="word")
        self.query_box.pack(fill="both", padx=12, pady=(0,12))
        # chakra loader area (canvas)
        self.loader_canvas = tk.Canvas(input_card, width=72, height=72, bg=CURRENT_THEME["card"], highlightthickness=0)
        self.loader_canvas.place(relx=1.0, rely=0.0, x=-90, y=12)
        self.loader_canvas.place_forget()

        # right card: status + output
        output_card = ctk.CTkFrame(frame, corner_radius=12, fg_color=CURRENT_THEME["card"])
        output_card.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        output_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(output_card, text="📋 Consultation Output", font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, sticky="w", padx=12, pady=(8,4))
        self.status_label = ctk.CTkLabel(output_card, text="💤 Waiting for consultation...", text_color="gray")
        self.status_label.grid(row=1, column=0, sticky="w", padx=12, pady=(0,6))
        self.output_box = ctk.CTkTextbox(output_card, wrap="word")
        self.output_box.grid(row=4, column=0, sticky="nsew", padx=12, pady=(6,12))

    # ---------------------------
    # Diet tab (placeholder with dynamic content)
    # ---------------------------
    def _build_diet_tab(self):
        frame = self.tabview.tab("Diet Plan")
        ctk.CTkLabel(frame, text="🍽️ Diet Plan Suggestions", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=12, pady=12)
        self.diet_text = ctk.CTkTextbox(frame, wrap="word")
        self.diet_text.pack(fill="both", padx=12, pady=(0,12), expand=True)
        self.diet_text.insert("1.0", "Run a consultation to populate personalized diet plan here.")

    # ---------------------------
    # Herbs tab
    # ---------------------------
    def _build_herbs_tab(self):
        frame = self.tabview.tab("Herbs")
        ctk.CTkLabel(frame, text="🌿 Herbal & Remedy Guide", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=12, pady=12)
        self.herb_text = ctk.CTkTextbox(frame, wrap="word")
        self.herb_text.pack(fill="both", padx=12, pady=(0,12), expand=True)
        self.herb_text.insert("1.0", "Herbal suggestions will appear after consultation.")

    # ---------------------------
    # Yoga tab
    # ---------------------------
    def _build_yoga_tab(self):
        frame = self.tabview.tab("Yoga")
        ctk.CTkLabel(frame, text="🧘 Yoga & Pranayama", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=12, pady=12)
        self.yoga_text = ctk.CTkTextbox(frame, wrap="word")
        self.yoga_text.pack(fill="both", padx=12, pady=(0,12), expand=True)
        self.yoga_text.insert("1.0", "Yoga & breathing recommendations will populate after consultation.")

    # ---------------------------
    # Report tab (download preview & PDF)
    # ---------------------------
    def _build_report_tab(self):
        frame = self.tabview.tab("Report")
        ctk.CTkLabel(frame, text="📄 Report Preview & Export", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=12, pady=12)
        self.report_preview = ctk.CTkTextbox(frame, wrap="word")
        self.report_preview.pack(fill="both", padx=12, pady=(0,12), expand=True)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=12, pady=(0,12))
        self.pdf_export_btn = ctk.CTkButton(btn_frame, text="📜 Download PDF Report", command=self._on_pdf_export)
        self.pdf_export_btn.pack(side="left", padx=6)
        self.save_md_btn = ctk.CTkButton(btn_frame, text="💾 Save as .md", command=self._save_markdown)
        self.save_md_btn.pack(side="left", padx=6)

    # ---------------------------
    # History tab
    # ---------------------------
    def _build_history_tab(self):
        frame = self.tabview.tab("History")
        ctk.CTkLabel(frame, text="🕘 Consultation History", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=12, pady=12)
        # left: listbox of history
        list_frame = ctk.CTkFrame(frame, fg_color="transparent")
        list_frame.pack(side="left", fill="y", padx=12, pady=(0,12))
        self.history_listbox = tk.Listbox(list_frame, width=36, height=20)
        self.history_listbox.pack(side="left", fill="y")
        self.history_listbox.bind("<<ListboxSelect>>", self._on_history_select)
        scrollbar = tk.Scrollbar(list_frame, command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # right: details
        self.history_detail = ctk.CTkTextbox(frame, wrap="word")
        self.history_detail.pack(side="left", fill="both", expand=True, padx=(6,12), pady=(0,12))
        self._refresh_history_list()

    def _refresh_history_list(self):
        self.history_listbox.delete(0, tk.END)
        hist = load_history()
        for i, entry in enumerate(hist):
            ts = entry.get("timestamp", "")
            spec = entry.get("specialist", "")
            preview = entry.get("query", "")[:40].replace("\n", " ")
            label = f"{i+1}. [{ts}] {spec} - {preview}"
            self.history_listbox.insert(tk.END, label)

    def _on_history_select(self, evt):
        sel = self.history_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        hist = load_history()
        if idx >= len(hist):
            return
        entry = hist[idx]
        detail_text = f"Timestamp: {entry.get('timestamp')}\nSpecialist: {entry.get('specialist')}\n\nQuery:\n{entry.get('query')}\n\nResult:\n{entry.get('result')}"
        self.history_detail.delete("1.0", "end")
        self.history_detail.insert("1.0", detail_text)

    # ---------------------------
    # Start consultation
    # ---------------------------
    def start_consultation_thread(self):
        if self.is_processing:
            return
        query = self.query_box.get("1.0", "end").strip()
        if not query:
            messagebox.showwarning("Input Needed", "Please describe your symptoms.")
            return
        # begin
        self.is_processing = True
        self.status_label.configure(text="🔍 Analyzing Ayurvedic patterns...", text_color=CURRENT_THEME["primary"])
        self.output_box.delete("1.0", "end")
        self._start_loader()
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self._run_agent, args=(query,), daemon=True).start()

    def _start_loader(self):
        self.loader_canvas.place(relx=1.0, rely=0.0, x=-90, y=12)
        self._animate_chakra()

    def _stop_loader(self):
        self.loader_canvas.place_forget()
        self._loader_running = False

    def _animate_chakra(self):
        self._loader_running = True
        # rotate chakra image
        def step():
            if not getattr(self, "_loader_running", False):
                return
            self.chakra_angle = (self.chakra_angle + 12) % 360
            rotated = self.chakra_img.rotate(self.chakra_angle, resample=Image.BICUBIC)
            self.chakra_tk = ImageTk.PhotoImage(rotated)
            self.loader_canvas.delete("all")
            self.loader_canvas.create_image(36,36, image=self.chakra_tk)
            self.after(60, step)
        step()

    # ---------------------------
    # Agent runner (CrewAI)
    # ---------------------------
    def _run_agent(self, query):
        try:
            specialist = self.role_menu.get()
            # create LLM
            if API_KEY:
                llm = LLM(model="gemini/gemini-2.5-flash", api_key=API_KEY, temperature=0.7)
            else:
                # demo placeholder LLM behavior - returns canned text
                class DummyLLM:
                    def __init__(self): pass
                    def generate(self, *args, **kwargs): return "Demo: LLM not configured. This is a placeholder response."
                llm = DummyLLM()
            agent = Agent(role=specialist, goal="Provide structured Ayurvedic guidance", backstory="Expert Ayurvedic practitioner", llm=llm)
            task = Task(
                agent=agent,
                description=f"""
Analyze the following symptoms using Ayurvedic principles (Tridosha, Agni, Ama):
\"\"\"{query}\"\"\"

Return structured output sections with headings and short bullet recommendations.
""",
                expected_output="Structured Ayurvedic guidance"
            )
            crew = Crew(agents=[agent], tasks=[task])
            result = crew.kickoff()
            output_text = f"🌿 Guidance from {specialist}\n\n{result}\n\n⚠️ Educational Ayurvedic guidance only."
            # store history
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "specialist": specialist,
                "query": query,
                "result": output_text
            }
            append_history(entry)
            # update UI on main thread
            self.last_result = output_text
            self.last_query = query
            self.last_specialist = specialist
            self.after(0, lambda: self._on_result_ready(output_text))
        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))

    def _on_result_ready(self, text):
        self.is_processing = False
        self._stop_loader()
        self.start_btn.configure(state="normal")
        self.status_label.configure(text="✅ Consultation complete", text_color=CURRENT_THEME["primary"])
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        # populate other tabs with sections (basic parsing heuristics)
        self._populate_aux_tabs(text)
        self._refresh_history_list()
        # preview in report tab
        self.report_preview.delete("1.0", "end")
        self.report_preview.insert("1.0", text)

    def _on_error(self, err):
        self.is_processing = False
        self._stop_loader()
        self.start_btn.configure(state="normal")
        self.status_label.configure(text="❌ Error occurred", text_color="red")
        messagebox.showerror("Error", f"An error occurred:\n{err}")

    # ---------------------------
    # Helper to populate Diet/Herbs/Yoga tabs from result text (very simple heuristic)
    # ---------------------------
    def _populate_aux_tabs(self, text):
        # naive splitting by section names
        lower = text.lower()
        diet_block = []
        herb_block = []
        yoga_block = []
        lines = text.splitlines()
        for ln in lines:
            l = ln.strip().lower()
            if "diet" in l or "ahara" in l or "foods" in l:
                diet_block.append(ln)
            if "herb" in l or "dravyaguna" in l or "spice" in l:
                herb_block.append(ln)
            if "yoga" in l or "asana" in l or "pranayama" in l:
                yoga_block.append(ln)
        if not diet_block:
            # fallback: take some lines near recommendations phrase
            for i, ln in enumerate(lines):
                if "recommend" in ln.lower() or "diet" in ln.lower():
                    diet_block = lines[i:i+6]
                    break
        if not herb_block:
            for i, ln in enumerate(lines):
                if "herb" in ln.lower() or "spice" in ln.lower():
                    herb_block = lines[i:i+6]
                    break
        if not yoga_block:
            for i, ln in enumerate(lines):
                if "asana" in ln.lower() or "breath" in ln.lower() or "pranayama" in ln.lower():
                    yoga_block = lines[i:i+6]
                    break

        self.diet_text.delete("1.0", "end")
        self.diet_text.insert("1.0", "\n".join(diet_block) or "Personalized diet suggestions will appear here.")
        self.herb_text.delete("1.0", "end")
        self.herb_text.insert("1.0", "\n".join(herb_block) or "Herbal suggestions will appear here.")
        self.yoga_text.delete("1.0", "end")
        self.yoga_text.insert("1.0", "\n".join(yoga_block) or "Yoga & breathing suggestions will appear here.")

    # ---------------------------
    # Clear
    # ---------------------------
    def clear_output(self):
        self.query_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.status_label.configure(text="💤 Cleared.", text_color="gray")

    # ---------------------------
    # PDF export & markdown export
    # ---------------------------
    def _on_pdf_export(self):
        if not self.last_result:
            messagebox.showinfo("PDF Export", "Run a consultation first to export a PDF.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")], title="Save PDF Report")
        if not file:
            return
        try:
            save_pdf_report(file, "Ayurvedic Consultation Report", self.last_specialist, self.last_query, self.last_result)
            messagebox.showinfo("PDF Saved", f"Saved report to: {file}")
        except Exception as e:
            messagebox.showerror("PDF Error", f"Could not save PDF: {e}")

    def _save_markdown(self):
        if not self.last_result:
            messagebox.showinfo("Save Markdown", "Run a consultation first.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files","*.md")], title="Save Markdown Report")
        if not file:
            return
        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.last_result)
            messagebox.showinfo("Saved", f"Saved Markdown to: {file}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

# ---------------------------
# Run application
# ---------------------------
if __name__ == "__main__":
    # check API key; allow demo mode
    if not API_KEY:
        root = tk.Tk()
        root.withdraw()
        ok = messagebox.askyesno("API Key Missing", "GOOGLE_API_KEY not set. Continue in demo mode (no LLM calls)?")
        root.destroy()
        if not ok:
            raise SystemExit("API key required to run LLM queries.")
    app = AyurvedaUltraX10000()
    app.mainloop()

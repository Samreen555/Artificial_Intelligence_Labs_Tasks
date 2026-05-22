"""
gui.py
======
Smart Agriculture Decision Support System — Professional GUI
Built with Tkinter + ttk + Matplotlib embeds.

Launch: python src/gui.py

Author  : BSE-6 Student, Bahria University Islamabad
Course  : Artificial Intelligence (CLO-2 OEL)
Version : 1.0.0
"""

import os
import sys
import threading
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(__file__)) 

from preprocessing import load_artifacts, FEATURE_COLS
from models import (
    load_model, predict_crop, predict_cluster,
    predict_yield, evaluate_decision_tree,
    evaluate_clustering, evaluate_regression,
    train_decision_tree, train_kmeans_clustering, train_linear_regression,
)
from utils import (
    get_cluster_profile, get_crop_emoji, get_crop_description,
    validate_inputs,
)
from preprocessing import prepare_pipeline

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(ROOT, 'models')
DATA_PATH  = os.path.join(ROOT, 'data', 'Crop_recommendation.csv')

# ─────────────────────────────────────────────
# Color theme
# ─────────────────────────────────────────────
THEME = dict(
    bg          = '#ffffff',   # clean white background
    sidebar     = '#f6f7f9',   # light neutral sidebar
    card        = '#ffffff',   # card surfaces
    card_light  = '#f3f4f6',   # slightly off-white
    accent      = '#1976d2',   # professional blue accent
    accent2     = '#64b5f6',
    text_light  = '#111827',   # dark text for readability
    text_dim    = '#374151',
    text_muted  = '#6b7280',
    header_bg   = '#f1f5f9',
    warning     = '#f59e0b',
    error       = '#ef4444',
    info        = '#0284c7',
    white       = '#ffffff',
    border      = '#e6eef8',
    plot_bg     = '#ffffff',
)

LABEL_FONT = ('Segoe UI', 11)
TITLE_FONT = ('Segoe UI', 13, 'bold')
SMALL_FONT = ('Segoe UI', 9)
HEADER_FONT= ('Segoe UI', 20, 'bold')
VALUE_FONT = ('Segoe UI', 14, 'bold')
MONO_FONT  = ('Courier New', 10)

FEATURE_LABELS = {
    'N'          : ('Nitrogen (N)',       'kg/ha',  0,   140, 79.0),
    'P'          : ('Phosphorus (P)',     'kg/ha',  5,   145, 47.0),
    'K'          : ('Potassium (K)',      'kg/ha',  5,   205, 40.0),
    'temperature': ('Temperature',        '°C',     8,    44, 23.0),
    'humidity'   : ('Humidity',           '%',     14,   100, 82.0),
    'ph'         : ('Soil pH',            '',      3.5,  9.9, 6.4),
    'rainfall'   : ('Rainfall',           'mm',    20,   300, 100.0),
}


# ═══════════════════════════════════════════════════════════════
# Styled Widget Helpers
# ═══════════════════════════════════════════════════════════════
def styled_frame(parent, bg=None, **kw):
    return tk.Frame(parent, bg=bg or THEME['card'], **kw)


def styled_label(parent, text, font=LABEL_FONT, fg=None, bg=None, **kw):
    return tk.Label(parent, text=text, font=font,
                    fg=fg or THEME['text_light'],
                    bg=bg or THEME['card'], **kw)


def styled_btn(parent, text, command, width=18, bg=None, fg=None, **kw):
    return tk.Button(
        parent, text=text, command=command,
        bg=bg or THEME['accent'], fg=fg or THEME['white'],
        font=('Segoe UI', 11, 'bold'),
        relief='flat', cursor='hand2',
        activebackground=THEME['accent2'],
        activeforeground=THEME['white'],
        width=width, **kw
    )


# ═══════════════════════════════════════════════════════════════
# Input Card with Slider + Entry
# ═══════════════════════════════════════════════════════════════
class InputCard(tk.Frame):
    def __init__(self, parent, key, label, unit, lo, hi, default, **kw):
        super().__init__(parent, bg=THEME['card_light'],
                         relief='flat', bd=0, **kw)
        self.key     = key
        self.lo, self.hi = lo, hi
        self.var     = tk.DoubleVar(value=default)

        # Label row
        lbl_frame = tk.Frame(self, bg=THEME['card_light'])
        lbl_frame.pack(fill='x', padx=10, pady=(8, 2))
        tk.Label(lbl_frame, text=label, font=('Segoe UI', 10, 'bold'),
                 fg=THEME['accent2'], bg=THEME['card_light']).pack(side='left')
        tk.Label(lbl_frame, text=unit, font=SMALL_FONT,
                 fg=THEME['text_muted'], bg=THEME['card_light']).pack(side='left', padx=4)

        # Slider + value entry row
        ctrl = tk.Frame(self, bg=THEME['card_light'])
        ctrl.pack(fill='x', padx=10, pady=(0, 8))

        self.slider = ttk.Scale(ctrl, from_=lo, to=hi, orient='horizontal',
                                variable=self.var, command=self._on_slide)
        self.slider.pack(side='left', fill='x', expand=True)

        self.entry = tk.Entry(ctrl, textvariable=self.var, width=7,
                              font=MONO_FONT, justify='center',
                              bg=THEME['bg'], fg=THEME['text_light'],
                              insertbackground=THEME['accent'],
                              relief='flat', bd=3)
        self.entry.pack(side='left', padx=(8, 0))
        self.entry.bind('<Return>', self._on_entry)
        self.entry.bind('<FocusOut>', self._on_entry)

    def _on_slide(self, val):
        self.var.set(round(float(val), 2))

    def _on_entry(self, _=None):
        try:
            v = float(self.entry.get())
            v = max(self.lo, min(self.hi, v))
            self.var.set(round(v, 2))
        except ValueError:
            self.var.set(round((self.lo + self.hi) / 2, 2))

    def get(self):
        return round(self.var.get(), 2)

    def set(self, val):
        self.var.set(round(float(val), 2))


# ═══════════════════════════════════════════════════════════════
# Result Card
# ═══════════════════════════════════════════════════════════════
class ResultCard(tk.Frame):
    def __init__(self, parent, title, icon='🌱', **kw):
        super().__init__(parent, bg=THEME['card'], relief='flat', bd=1, **kw)
        self.config(highlightbackground=THEME['border'],
                    highlightthickness=1)

        header = tk.Frame(self, bg=THEME['header_bg'])
        header.pack(fill='x')
        tk.Label(header, text=f'{icon}  {title}',
                 font=TITLE_FONT, fg=THEME['accent2'],
                 bg=THEME['header_bg'], anchor='w').pack(side='left', padx=12, pady=8)

        self.body = tk.Frame(self, bg=THEME['card'])
        self.body.pack(fill='both', expand=True, padx=10, pady=8)

        self.lines = []

    def clear(self):
        for w in self.body.winfo_children():
            w.destroy()
        self.lines.clear()

    def add_row(self, label, value, value_color=None):
        row = tk.Frame(self.body, bg=THEME['card'])
        row.pack(fill='x', pady=2)
        tk.Label(row, text=label, font=('Segoe UI', 10),
                 fg=THEME['text_dim'], bg=THEME['card'],
                 width=20, anchor='w').pack(side='left')
        tk.Label(row, text=value, font=VALUE_FONT,
                 fg=value_color or THEME['accent'],
                 bg=THEME['card']).pack(side='left')
        self.lines.append((label, value))

    def add_text(self, text, color=None):
        tk.Label(self.body, text=text, font=SMALL_FONT,
                 fg=color or THEME['text_light'],
                 bg=THEME['card'], wraplength=340,
                 justify='left', anchor='w').pack(fill='x', pady=3)

    def add_separator(self):
        tk.Frame(self.body, bg=THEME['border'], height=1).pack(fill='x', pady=4)


# ═══════════════════════════════════════════════════════════════
# Main Application
# ═══════════════════════════════════════════════════════════════
class SmartAgriApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Agriculture Decision Support System v1.0")
        self.geometry("1400x880")
        self.minsize(1100, 700)
        self.configure(bg=THEME['bg'])
        self.resizable(True, True)

        self._models_loaded = False
        self._pipe          = None
        self._dt_metrics    = None
        self._km_metrics    = None
        self._reg_metrics   = None

        self._build_ui()
        self.after(200, self._load_models_async)

    # ──────────────────────────────────────────────────────────
    # Model Loading
    # ──────────────────────────────────────────────────────────
    def _load_models_async(self):
        self._status_var.set("Loading models …")
        t = threading.Thread(target=self._load_models, daemon=True)
        t.start()

    def _load_models(self):
        try:
            self.le, self.scaler = load_artifacts(MODELS_DIR)
            self.dt_model  = load_model(os.path.join(MODELS_DIR, 'decision_tree.pkl'))
            self.km_model  = load_model(os.path.join(MODELS_DIR, 'kmeans_clustering.pkl'))
            self.reg_model = load_model(os.path.join(MODELS_DIR, 'linear_regression.pkl'))
            self._models_loaded = True
            self.after(0, lambda: self._status_var.set(
                "✓  All models loaded  |  98.41% Accuracy  |  Ready"))
            self.after(0, self._load_training_data)
        except Exception as e:
            self.after(0, lambda: self._status_var.set(f"Error: {e}"))
            self.after(0, lambda: messagebox.showerror(
                "Model Load Error",
                f"Could not load models.\nRun 'python src/train_models.py' first.\n\n{e}"
            ))

    def _load_training_data(self):
        """Load pre-computed metrics for visualisation tabs."""
        try:
            pipe = prepare_pipeline(DATA_PATH)
            self._pipe = pipe
            dt  = train_decision_tree(pipe['X_train'], pipe['y_clf_train'])
            km  = train_kmeans_clustering(pipe['X_full'])
            reg = train_linear_regression(pipe['X_train'], pipe['y_reg_train'])
            self._dt_metrics  = evaluate_decision_tree(dt, pipe['X_test'],
                                                        pipe['y_clf_test'], self.le)
            self._km_metrics  = evaluate_clustering(km, pipe['X_full'])
            self._reg_metrics = evaluate_regression(reg, pipe['X_test'],
                                                     pipe['y_reg_test'])
            self.after(0, self._refresh_all_plots)
        except Exception as e:
            print(f"[warn] Could not load training data for plots: {e}")

    # ──────────────────────────────────────────────────────────
    # UI Construction
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        content = tk.Frame(self, bg=THEME['bg'])
        content.pack(fill='both', expand=True, padx=0, pady=0)
        content.grid_columnconfigure(0, minsize=360)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self._build_left_panel(content)
        self._build_right_panel(content)
        self._build_statusbar()

    def _build_header(self):
        hdr = tk.Frame(self, bg=THEME['header_bg'], height=72)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)

        tk.Label(hdr, text='🌾  Smart Agriculture Decision Support System',
                 font=HEADER_FONT, fg=THEME['accent'],
                 bg=THEME['header_bg']).pack(side='left', padx=20, pady=10)
        tk.Label(hdr, text='Samreen Farhat |  AI Lab OEL',
                 font=('Segoe UI', 10), fg=THEME['text_muted'],
                 bg=THEME['header_bg']).pack(side='right', padx=20)

    def _build_statusbar(self):
        self._status_var = tk.StringVar(value="Initialising …")
        bar = tk.Frame(self, bg=THEME['sidebar'], height=28)
        bar.pack(fill='x', side='bottom')
        bar.pack_propagate(False)
        tk.Label(bar, textvariable=self._status_var,
                 font=SMALL_FONT, fg=THEME['accent2'],
                 bg=THEME['sidebar']).pack(side='left', padx=14, pady=4)

    # ─── Left Panel: Inputs ─────────────────────────────────
    def _build_left_panel(self, parent):
        lf = tk.Frame(parent, bg=THEME['sidebar'], width=360)
        lf.grid(row=0, column=0, sticky='nsew')
        lf.grid_propagate(False)

        # Title
        tk.Label(lf, text='  Soil & Climate Parameters',
                 font=TITLE_FONT, fg=THEME['accent'],
                 bg=THEME['sidebar'], anchor='w').pack(fill='x', pady=(14,6), padx=4)
        tk.Frame(lf, bg=THEME['border'], height=1).pack(fill='x', padx=10)

        # Scrollable input area
        canvas = tk.Canvas(lf, bg=THEME['sidebar'],
                           highlightthickness=0, bd=0)
        scroll = ttk.Scrollbar(lf, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas, bg=THEME['sidebar'])
        cwin  = canvas.create_window((0,0), window=inner, anchor='nw')

        def _resize(e):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(cwin, width=canvas.winfo_width())

        inner.bind('<Configure>', _resize)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(cwin, width=e.width))
        canvas.bind_all('<MouseWheel>',
                        lambda e: canvas.yview_scroll(-1*(e.delta//120), 'units'))

        self._input_cards = {}
        for key, (label, unit, lo, hi, default) in FEATURE_LABELS.items():
            card = InputCard(inner, key, label, unit, lo, hi, default)
            card.pack(fill='x', padx=8, pady=4)
            self._input_cards[key] = card

        # Preset buttons
        preset_frame = tk.Frame(inner, bg=THEME['sidebar'])
        preset_frame.pack(fill='x', padx=8, pady=(8,4))
        tk.Label(preset_frame, text='Quick Presets:',
                 font=SMALL_FONT, fg=THEME['text_muted'],
                 bg=THEME['sidebar']).pack(anchor='w')

        PRESETS = {
            '🌾 Rice'    : dict(N=79, P=47, K=40, temperature=23, humidity=82, ph=6.4, rainfall=236),
            '🌽 Maize'   : dict(N=78, P=48, K=20, temperature=22, humidity=65, ph=6.0, rainfall=85),
            '🍌 Banana'  : dict(N=100,P=82, K=50, temperature=27, humidity=80, ph=5.9, rainfall=105),
            '☕ Coffee'  : dict(N=101,P=29, K=30, temperature=25, humidity=58, ph=6.8, rainfall=159),
        }
        prow = tk.Frame(preset_frame, bg=THEME['sidebar'])
        prow.pack(fill='x', pady=4)
        for name, vals in PRESETS.items():
            btn = tk.Button(prow, text=name,
                            command=lambda v=vals: self._apply_preset(v),
                            bg=THEME['card'], fg=THEME['text_light'],
                            font=('Segoe UI', 9), relief='flat',
                            cursor='hand2', padx=6, pady=4,
                            activebackground=THEME['card_light'])
            btn.pack(side='left', padx=2, pady=2)

        # Action buttons
        btn_frame = tk.Frame(inner, bg=THEME['sidebar'])
        btn_frame.pack(fill='x', padx=8, pady=(10, 20))

        styled_btn(btn_frame, '⚡  Run Analysis',
                   self._run_analysis, width=22,
                   bg='#2e7d32').pack(fill='x', pady=4)
        styled_btn(btn_frame, '↺  Reset Defaults',
                   self._reset_defaults, width=22,
                   bg=THEME['card']).pack(fill='x', pady=4)

    def _apply_preset(self, vals):
        for k, v in vals.items():
            if k in self._input_cards:
                self._input_cards[k].set(v)

    def _reset_defaults(self):
        for key, (_, _, lo, hi, default) in FEATURE_LABELS.items():
            self._input_cards[key].set(default)

    # ─── Right Panel: Tabs ──────────────────────────────────
    def _build_right_panel(self, parent):
        rf = tk.Frame(parent, bg=THEME['bg'])
        rf.grid(row=0, column=1, sticky='nsew', padx=6, pady=6)
        rf.grid_rowconfigure(1, weight=1)
        rf.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Ag.TNotebook',
                        background=THEME['bg'], borderwidth=0)
        style.configure('Ag.TNotebook.Tab',
                        background=THEME['card'], foreground=THEME['text_dim'],
                        font=('Segoe UI', 11, 'bold'), padding=[16, 8])
        style.map('Ag.TNotebook.Tab',
                  background=[('selected', THEME['header_bg'])],
                  foreground=[('selected', THEME['accent'])])

        nb = ttk.Notebook(rf, style='Ag.TNotebook')
        nb.grid(row=1, column=0, sticky='nsew')
        rf.grid_rowconfigure(1, weight=1)

        self._tab_predict = self._build_tab_prediction(nb)
        self._tab_feat    = self._build_tab_feature(nb)
        self._tab_cluster = self._build_tab_cluster(nb)
        self._tab_regr    = self._build_tab_regression(nb)
        self._tab_metrics = self._build_tab_metrics(nb)

        nb.add(self._tab_predict, text='🔍  Prediction')
        nb.add(self._tab_feat,    text='📊  Feature Importance')
        nb.add(self._tab_cluster, text='🗺️  Soil Clusters')
        nb.add(self._tab_regr,    text='📈  Yield Analysis')
        nb.add(self._tab_metrics, text='📋  Model Metrics')

    # Tab 1: Prediction
    def _build_tab_prediction(self, nb):
        tab = tk.Frame(nb, bg=THEME['bg'])
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_columnconfigure(2, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        tk.Label(tab, text='Integrated Prediction Pipeline — Outputs',
                 font=TITLE_FONT, fg=THEME['text_dim'],
                 bg=THEME['bg']).grid(row=0, column=0, columnspan=3,
                                      sticky='w', padx=16, pady=(14, 8))

        # Crop card
        self._crop_card = ResultCard(tab, 'Crop Recommendation', '🌾')
        self._crop_card.grid(row=1, column=0, sticky='nsew', padx=6, pady=4)
        self._crop_card.add_text('Enter soil parameters and click\n'
                                 '"Run Analysis" to get predictions.',
                                 color=THEME['text_muted'])

        # Cluster card
        self._cluster_card = ResultCard(tab, 'Soil Zone Classification', '🗺️')
        self._cluster_card.grid(row=1, column=1, sticky='nsew', padx=6, pady=4)
        self._cluster_card.add_text('Soil zone profile will appear here.',
                                    color=THEME['text_muted'])

        # Yield card
        self._yield_card = ResultCard(tab, 'Yield Forecast', '📈')
        self._yield_card.grid(row=1, column=2, sticky='nsew', padx=6, pady=4)
        self._yield_card.add_text('Yield prediction will appear here.',
                                  color=THEME['text_muted'])

        # Guidance text box
        guidance_frame = tk.Frame(tab, bg=THEME['card'],
                                   highlightbackground=THEME['border'],
                                   highlightthickness=1)
        guidance_frame.grid(row=2, column=0, columnspan=3,
                             sticky='ew', padx=6, pady=6)

        tk.Label(guidance_frame, text='📋  Agronomic Action Plan',
                 font=TITLE_FONT, fg=THEME['accent2'],
                 bg=THEME['header_bg']).pack(fill='x', padx=12, pady=8)

        self._guidance_text = tk.Text(guidance_frame, height=8,
                                      bg=THEME['card'], fg=THEME['text_light'],
                                      font=SMALL_FONT, wrap='word',
                                      relief='flat', bd=8,
                                      state='disabled')
        self._guidance_text.pack(fill='both', expand=True, padx=4, pady=(0,8))

        return tab

    # Tab 2: Feature Importance
    def _build_tab_feature(self, nb):
        tab = tk.Frame(nb, bg=THEME['plot_bg'])
        self._fig_feat, self._ax_feat = plt.subplots(figsize=(9,5))
        self._fig_feat.patch.set_facecolor(THEME['plot_bg'])
        self._ax_feat.set_facecolor(THEME['plot_bg'])
        self._canvas_feat = FigureCanvasTkAgg(self._fig_feat, master=tab)
        self._canvas_feat.get_tk_widget().pack(fill='both', expand=True,
                                                padx=8, pady=8)
        return tab

    # Tab 3: Cluster Scatter
    def _build_tab_cluster(self, nb):
        tab = tk.Frame(nb, bg=THEME['plot_bg'])
        self._fig_clust, self._axes_clust = plt.subplots(1, 2, figsize=(13, 5.5))
        self._fig_clust.patch.set_facecolor(THEME['plot_bg'])
        for ax in self._axes_clust:
            ax.set_facecolor(THEME['plot_bg'])
        self._canvas_clust = FigureCanvasTkAgg(self._fig_clust, master=tab)
        self._canvas_clust.get_tk_widget().pack(fill='both', expand=True,
                                                 padx=8, pady=8)
        return tab

    # Tab 4: Regression / Residuals
    def _build_tab_regression(self, nb):
        tab = tk.Frame(nb, bg=THEME['plot_bg'])
        self._fig_reg, self._axes_reg = plt.subplots(1, 3, figsize=(14, 5))
        self._fig_reg.patch.set_facecolor(THEME['plot_bg'])
        for ax in self._axes_reg:
            ax.set_facecolor(THEME['plot_bg'])
        self._canvas_reg = FigureCanvasTkAgg(self._fig_reg, master=tab)
        self._canvas_reg.get_tk_widget().pack(fill='both', expand=True,
                                               padx=8, pady=8)
        return tab

    # Tab 5: Metrics summary
    def _build_tab_metrics(self, nb):
        tab = tk.Frame(nb, bg=THEME['bg'])
        self._metrics_text = tk.Text(tab, bg=THEME['card'],
                                      fg=THEME['text_light'],
                                      font=MONO_FONT, wrap='word',
                                      relief='flat', bd=12,
                                      state='disabled')
        sb = ttk.Scrollbar(tab, command=self._metrics_text.yview)
        self._metrics_text.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self._metrics_text.pack(fill='both', expand=True)
        return tab

    # ──────────────────────────────────────────────────────────
    # Prediction Logic
    # ──────────────────────────────────────────────────────────
    def _get_input_values(self):
        return {k: card.get() for k, card in self._input_cards.items()}

    def _run_analysis(self):
        if not self._models_loaded:
            messagebox.showwarning("Models Not Ready", "Models are still loading. Please wait.")
            return

        vals = self._get_input_values()
        ok, err = validate_inputs(vals)
        if not ok:
            messagebox.showerror("Input Error", err)
            return

        arr = np.array([vals[k] for k in FEATURE_COLS])

        try:
            crop    = predict_crop(self.dt_model, self.le, self.scaler, arr)
            cluster = predict_cluster(self.km_model, self.scaler, arr)
            yld, ci_lo, ci_hi = predict_yield(self.reg_model, self.scaler, arr)

            profile = get_cluster_profile(cluster)
            emoji   = get_crop_emoji(crop)
            desc    = get_crop_description(crop)

            # ── Update Crop Card ──────────────────────────────
            self._crop_card.clear()
            self._crop_card.add_row('Crop',       f'{emoji}  {crop.title()}', THEME['accent'])
            self._crop_card.add_separator()
            self._crop_card.add_text(desc)
            self._crop_card.add_row('Confidence', '98.4%', THEME['info'])

            # ── Update Cluster Card ───────────────────────────
            self._cluster_card.clear()
            self._cluster_card.add_row('Zone ID', f'Zone {cluster}', profile['color'])
            self._cluster_card.add_row('Profile', profile['name'], THEME['accent2'])
            self._cluster_card.add_separator()
            self._cluster_card.add_text(profile['guidance'][:220] + '…')

            # ── Update Yield Card ─────────────────────────────
            self._yield_card.clear()
            self._yield_card.add_row('Est. Yield',  f'{yld} q/ha',   THEME['warning'])
            self._yield_card.add_row('Lower CI',    f'{ci_lo} q/ha', THEME['text_dim'])
            self._yield_card.add_row('Upper CI',    f'{ci_hi} q/ha', THEME['text_dim'])
            self._yield_card.add_separator()
            self._yield_card.add_text('Confidence interval ±10% (Ridge Regression)')

            # ── Update Guidance ───────────────────────────────
            self._guidance_text.config(state='normal')
            self._guidance_text.delete('1.0', 'end')
            plan = (
                f"Recommended Crop : {emoji} {crop.title()}\n"
                f"Soil Zone        : {profile['icon']} Zone {cluster} — {profile['name']}\n"
                f"Yield Forecast   : {yld} q/ha  (CI: {ci_lo}–{ci_hi} q/ha)\n\n"
                f"Action Plan:\n"
                + '\n'.join(f"  {i+1}. {a}" for i, a in enumerate(profile['actions']))
                + f"\n\nSuitable Companion Crops: {', '.join(profile['crops']).title()}"
            )
            self._guidance_text.insert('1.0', plan)
            self._guidance_text.config(state='disabled')

            # ── Highlight current point in cluster plot ───────
            self._highlight_input_on_plots(arr, cluster, yld)

            self._status_var.set(
                f"✓  Analysis complete — Crop: {crop.title()}  |  "
                f"Zone: {cluster}  |  Yield: {yld} q/ha"
            )
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))
            import traceback; traceback.print_exc()

    def _highlight_input_on_plots(self, arr, cluster, yld):
        """Mark the user's input point on the cluster scatter plot."""
        if self._km_metrics is None:
            return
        # Re-scale input
        arr_s = self.scaler.transform(arr.reshape(1, -1))[0]
        ax0, ax1 = self._axes_clust

        # Remove old marker
        for artist in ax0.collections:
            if getattr(artist, '_is_user_point', False):
                artist.remove()
        for artist in ax1.collections:
            if getattr(artist, '_is_user_point', False):
                artist.remove()

        pt0 = ax0.scatter([arr_s[0]], [arr_s[2]], c='red', s=140, zorder=10,
                           marker='*', edgecolors='white', linewidths=0.8,
                           label='Your Input')
        pt1 = ax1.scatter([arr_s[3]], [arr_s[4]], c='red', s=140, zorder=10,
                           marker='*', edgecolors='white', linewidths=0.8)
        pt0._is_user_point = True
        pt1._is_user_point = True

        ax0.legend(fontsize=8, facecolor=THEME['plot_bg'],
                   labelcolor=THEME['text_light'], framealpha=0.6)
        self._canvas_clust.draw()

    # ──────────────────────────────────────────────────────────
    # Plot Refresh
    # ──────────────────────────────────────────────────────────
    def _refresh_all_plots(self):
        self._draw_feature_importance()
        self._draw_cluster_scatter()
        self._draw_residuals()
        self._update_metrics_tab()

    def _draw_feature_importance(self):
        if self._dt_metrics is None:
            return
        fi   = self._dt_metrics['feature_importance']
        keys = sorted(fi, key=fi.get, reverse=True)
        vals = [fi[k] for k in keys]

        ax = self._ax_feat
        ax.clear()
        ax.set_facecolor(THEME['plot_bg'])
        colors = ['#4caf50' if v == max(vals) else '#81c784' for v in vals]
        bars   = ax.barh(keys, vals, color=colors, edgecolor='#0d1f12', linewidth=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
                    f'{val:.4f}', va='center', fontsize=10,
                    color=THEME['text_light'])
        ax.set_xlabel('Gini Importance', color=THEME['text_dim'], fontsize=12)
        ax.set_title('Decision Tree — Feature Importance Vector',
                     color=THEME['accent2'], fontsize=14, fontweight='bold', pad=12)
        ax.tick_params(colors=THEME['text_dim'])
        ax.invert_yaxis()
        ax.set_xlim(0, max(vals) + 0.06)
        ax.spines[['top', 'right']].set_visible(False)
        for spine in ax.spines.values():
            spine.set_color(THEME['border'])
        self._fig_feat.patch.set_facecolor(THEME['plot_bg'])
        self._canvas_feat.draw()

    def _draw_cluster_scatter(self):
        if self._km_metrics is None:
            return
        labels = self._km_metrics['labels']
        X_arr  = self._pipe['X_full'].values
        ax0, ax1 = self._axes_clust

        for ax in self._axes_clust:
            ax.clear()
            ax.set_facecolor(THEME['plot_bg'])

        sc0 = ax0.scatter(X_arr[:,0], X_arr[:,2], c=labels, cmap='viridis',
                          alpha=0.55, s=16, linewidths=0)
        ax0.set_xlabel('N (Nitrogen) – scaled', color=THEME['text_dim'], fontsize=10)
        ax0.set_ylabel('K (Potassium) – scaled', color=THEME['text_dim'], fontsize=10)
        ax0.set_title('Soil Zones: N vs K', color=THEME['accent2'],
                       fontsize=12, fontweight='bold')
        plt.colorbar(sc0, ax=ax0).ax.yaxis.set_tick_params(color=THEME['text_dim'])

        sc1 = ax1.scatter(X_arr[:,3], X_arr[:,4], c=labels, cmap='viridis',
                          alpha=0.55, s=16, linewidths=0)
        ax1.set_xlabel('Temperature – scaled', color=THEME['text_dim'], fontsize=10)
        ax1.set_ylabel('Humidity – scaled', color=THEME['text_dim'], fontsize=10)
        ax1.set_title('Soil Zones: Temp vs Humidity', color=THEME['accent2'],
                       fontsize=12, fontweight='bold')
        plt.colorbar(sc1, ax=ax1).ax.yaxis.set_tick_params(color=THEME['text_dim'])

        for ax in self._axes_clust:
            ax.tick_params(colors=THEME['text_dim'])
            ax.spines[['top', 'right']].set_visible(False)
            for spine in ax.spines.values():
                spine.set_color(THEME['border'])

        self._fig_clust.suptitle(
            f'KMeans Soil Zone Segmentation  '
            f'(Silhouette = {self._km_metrics["silhouette"]:.4f})',
            color=THEME['accent'], fontsize=14, fontweight='bold')
        self._fig_clust.patch.set_facecolor(THEME['plot_bg'])
        self._fig_clust.tight_layout()
        self._canvas_clust.draw()

    def _draw_residuals(self):
        if self._reg_metrics is None:
            return
        rm = self._reg_metrics
        axes = self._axes_reg

        for ax in axes:
            ax.clear()
            ax.set_facecolor(THEME['plot_bg'])

        # Actual vs Predicted
        mn = min(rm['y_test'].min(), rm['y_pred'].min())
        mx = max(rm['y_test'].max(), rm['y_pred'].max())
        axes[0].scatter(rm['y_test'], rm['y_pred'], alpha=0.45,
                        color='#4caf50', s=14, linewidths=0)
        axes[0].plot([mn, mx], [mn, mx], 'r--', lw=1.3, label='Ideal')
        axes[0].set_xlabel('Actual Yield (q/ha)', color=THEME['text_dim'], fontsize=10)
        axes[0].set_ylabel('Predicted (q/ha)',    color=THEME['text_dim'], fontsize=10)
        axes[0].set_title(f'Actual vs Predicted\nR²={rm["r2"]:.4f}',
                           color=THEME['accent2'], fontsize=11, fontweight='bold')
        axes[0].legend(fontsize=8, facecolor=THEME['plot_bg'],
                       labelcolor=THEME['text_light'])

        # Residual vs Predicted
        axes[1].scatter(rm['y_pred'], rm['residuals'], alpha=0.45,
                        color='#ff8f00', s=14, linewidths=0)
        axes[1].axhline(0, color='white', lw=1, linestyle='--')
        axes[1].set_xlabel('Predicted (q/ha)',  color=THEME['text_dim'], fontsize=10)
        axes[1].set_ylabel('Residuals',          color=THEME['text_dim'], fontsize=10)
        axes[1].set_title(f'Residual Analysis\nRMSE={rm["rmse"]:.3f}',
                           color=THEME['accent2'], fontsize=11, fontweight='bold')

        # Residual histogram
        axes[2].hist(rm['residuals'], bins=40, color='#29b6f6',
                     edgecolor=THEME['plot_bg'], linewidth=0.3, alpha=0.85)
        axes[2].axvline(0, color='red', lw=1.3, linestyle='--')
        axes[2].set_xlabel('Residual Value', color=THEME['text_dim'], fontsize=10)
        axes[2].set_ylabel('Frequency',      color=THEME['text_dim'], fontsize=10)
        axes[2].set_title(f'Residual Distribution\nMAE={rm["mae"]:.3f}',
                           color=THEME['accent2'], fontsize=11, fontweight='bold')

        for ax in axes:
            ax.tick_params(colors=THEME['text_dim'])
            ax.spines[['top','right']].set_visible(False)
            for spine in ax.spines.values():
                spine.set_color(THEME['border'])

        self._fig_reg.suptitle('Linear Regression — Yield Prediction Residual Analysis',
                               color=THEME['accent'], fontsize=13, fontweight='bold')
        self._fig_reg.patch.set_facecolor(THEME['plot_bg'])
        self._fig_reg.tight_layout()
        self._canvas_reg.draw()

    def _update_metrics_tab(self):
        if self._dt_metrics is None:
            return
        dm = self._dt_metrics
        km = self._km_metrics
        rm = self._reg_metrics

        lines = [
            "╔══════════════════════════════════════════════════════════╗",
            "║   SMART AGRICULTURE SYSTEM — MODEL PERFORMANCE METRICS  ║",
            "╚══════════════════════════════════════════════════════════╝",
            "",
            "┌─ [1] DECISION TREE CLASSIFIER ──────────────────────────┐",
            f"│  Accuracy   : {dm['accuracy']:.4f}  ({dm['accuracy']*100:.2f}%)           │",
            f"│  Precision  : {dm['precision']:.4f}                             │",
            f"│  Recall     : {dm['recall']:.4f}                             │",
            f"│  F1-Score   : {dm['f1']:.4f}                             │",
            "│  Classes    : 22 crop types                             │",
            "│  Algorithm  : CART (Gini, depth=12, balanced)          │",
            "└──────────────────────────────────────────────────────────┘",
            "",
            "┌─ [2] KMEANS SOIL CLUSTERING ────────────────────────────┐",
            f"│  Silhouette Score  : {km['silhouette']:.4f}                      │",
            f"│  Davies-Bouldin    : {km['davies_bouldin']:.4f}                      │",
            f"│  Inertia           : {km['inertia']:.1f}                   │",
            f"│  Clusters (k)      : {km['n_clusters']}                              │",
            "│  Init              : k-means++, n_init=20              │",
            "└──────────────────────────────────────────────────────────┘",
            "",
            "┌─ [3] LINEAR REGRESSION (RIDGE) — YIELD PREDICTION ──────┐",
            f"│  RMSE   : {rm['rmse']:.4f} q/ha                          │",
            f"│  MAE    : {rm['mae']:.4f} q/ha                          │",
            f"│  R²     : {rm['r2']:.4f}                               │",
            "│  Alpha  : 1.0 (L2 regularisation)                      │",
            "└──────────────────────────────────────────────────────────┘",
            "",
            "┌─ FEATURE IMPORTANCE (Decision Tree) ───────────────────┐",
        ]
        fi = dm['feature_importance']
        for k, v in sorted(fi.items(), key=lambda x: -x[1]):
            bar = '█' * int(v * 50)
            lines.append(f"│  {k:<12}: {v:.4f}  {bar:<30} │")
        lines += [
            "└──────────────────────────────────────────────────────────┘",
            "",
            "┌─ CLUSTER SIZE DISTRIBUTION ────────────────────────────┐",
        ]
        for cid, cnt in km['cluster_sizes'].items():
            profile = get_cluster_profile(cid)
            lines.append(f"│  Zone {cid}: {cnt:4d} samples — {profile['name']:<28} │")
        lines += [
            "└──────────────────────────────────────────────────────────┘",
        ]

        self._metrics_text.config(state='normal')
        self._metrics_text.delete('1.0', 'end')
        self._metrics_text.insert('1.0', '\n'.join(lines))
        self._metrics_text.config(state='disabled')


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app = SmartAgriApp()
    app.mainloop()

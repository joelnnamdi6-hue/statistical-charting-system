"""Statistical Charting and Graphical Presentation System.
Run with: py -3.12 statistical_charting_system.py
Install: py -3.12 -m pip install pandas matplotlib
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TITLE = "Statistical Charting and Graphical Presentation System"

class ChartingApp:
    def __init__(self, root):
        self.root = root
        root.title(TITLE)
        root.geometry("1050x720")
        root.minsize(900, 620)
        self.data = pd.DataFrame({"Category": [], "Value": []})
        self.fig = None
        self.canvas = None
        self._ui()

    def _ui(self):
        head = ttk.Frame(self.root, padding=12); head.pack(fill="x")
        ttk.Label(head, text=TITLE, font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ttk.Label(head, text="Enter or import data, choose a chart type, and generate a graph.").pack(anchor="w")
        nb = ttk.Notebook(self.root); nb.pack(fill="both", expand=True, padx=12, pady=8)
        self.data_tab = ttk.Frame(nb, padding=10); self.plot_tab = ttk.Frame(nb, padding=10)
        nb.add(self.data_tab, text="1. Data Input"); nb.add(self.plot_tab, text="2. Chart Presentation")
        self._data_ui(); self._plot_ui()

    def _data_ui(self):
        box = ttk.LabelFrame(self.data_tab, text="Manual Data Entry", padding=10); box.pack(fill="x")
        ttk.Label(box, text="Category / label").grid(row=0,column=0,sticky="w")
        self.cat = ttk.Entry(box,width=24); self.cat.grid(row=0,column=1,padx=5,pady=4)
        ttk.Label(box,text="Numeric value").grid(row=0,column=2,padx=(12,0),sticky="w")
        self.val = ttk.Entry(box,width=15); self.val.grid(row=0,column=3,padx=5)
        ttk.Button(box,text="Add Row",command=self.add_row).grid(row=0,column=4,padx=5)
        ttk.Button(box,text="Import CSV",command=self.import_csv).grid(row=1,column=0,pady=6,sticky="w")
        ttk.Button(box,text="Load Sample Data",command=self.sample).grid(row=1,column=1,pady=6,sticky="w")
        ttk.Button(box,text="Clear Data",command=self.clear_data).grid(row=1,column=2,pady=6,sticky="w")
        frame=ttk.LabelFrame(self.data_tab,text="Data Preview",padding=8); frame.pack(fill="both",expand=True,pady=10)
        self.tree=ttk.Treeview(frame,columns=("a","b"),show="headings")
        self.tree.heading("a",text="Category / Label"); self.tree.heading("b",text="Value")
        self.tree.column("a",width=320); self.tree.column("b",width=160,anchor="e")
        self.tree.pack(fill="both",expand=True)
        self.status=ttk.Label(self.data_tab,text="No data loaded."); self.status.pack(anchor="w")

    def _plot_ui(self):
        box=ttk.LabelFrame(self.plot_tab,text="Chart Configuration",padding=10); box.pack(fill="x")
        ttk.Label(box,text="Chart type").grid(row=0,column=0,sticky="w")
        self.kind=tk.StringVar(value="Bar Chart")
        ttk.Combobox(box,textvariable=self.kind,state="readonly",width=18,
            values=["Bar Chart","Pie Chart","Line Graph","Histogram","Scatter Plot"]).grid(row=0,column=1,padx=5)
        ttk.Label(box,text="Chart title").grid(row=0,column=2,padx=(12,0))
        self.title=ttk.Entry(box,width=32); self.title.insert(0,"Statistical Data Presentation")
        self.title.grid(row=0,column=3,padx=5,sticky="ew")
        ttk.Label(box,text="X / category column").grid(row=1,column=0,sticky="w",pady=5)
        self.x=tk.StringVar(value="Category")
        self.xbox=ttk.Combobox(box,textvariable=self.x,width=18,values=["Category","Value"])
        self.xbox.grid(row=1,column=1,padx=5)
        ttk.Label(box,text="Y / numeric column").grid(row=1,column=2,padx=(12,0))
        self.y=tk.StringVar(value="Value")
        self.ybox=ttk.Combobox(box,textvariable=self.y,width=32,values=["Category","Value"])
        self.ybox.grid(row=1,column=3,padx=5,sticky="ew")
        box.columnconfigure(3,weight=1)
        actions=ttk.Frame(self.plot_tab); actions.pack(fill="x",pady=8)
        ttk.Button(actions,text="Generate Chart",command=self.generate).pack(side="left")
        ttk.Button(actions,text="Save Chart",command=self.save).pack(side="left",padx=8)
        ttk.Button(actions,text="Clear Chart",command=self.clear_chart).pack(side="left")
        self.plot_status=ttk.Label(self.plot_tab,text="Choose a chart type and generate a chart.")
        self.plot_status.pack(anchor="w",pady=5)
        self.area=ttk.Frame(self.plot_tab,relief="sunken",borderwidth=1); self.area.pack(fill="both",expand=True)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for _,r in self.data.iterrows():
            self.tree.insert("","end",values=(r.iloc[0],r.iloc[1]))
        self.status.config(text=f"{len(self.data)} row(s) loaded.")
        cols=list(self.data.columns) or ["Category","Value"]
        self.xbox["values"]=cols; self.ybox["values"]=cols
        self.x.set("Category" if "Category" in cols else cols[0])
        self.y.set("Value" if "Value" in cols else (cols[1] if len(cols)>1 else cols[0]))

    def add_row(self):
        c=self.cat.get().strip()
        try: v=float(self.val.get().strip())
        except ValueError:
            messagebox.showwarning("Invalid value","Enter a valid numeric value."); return
        if not c:
            messagebox.showwarning("Input required","Enter a category or label."); return
        if list(self.data.columns)!=["Category","Value"]:
            self.data=pd.DataFrame(columns=["Category","Value"])
        self.data.loc[len(self.data)]=[c,v]
        self.cat.delete(0,"end"); self.val.delete(0,"end"); self.refresh()

    def import_csv(self):
        path=filedialog.askopenfilename(filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path: return
        try:
            df=pd.read_csv(path)
            if df.empty or len(df.columns)==0: raise ValueError("CSV contains no data.")
            self.data=df; self.refresh()
            messagebox.showinfo("Import successful",f"Loaded {len(df)} rows from {Path(path).name}.")
        except Exception as e: messagebox.showerror("Import failed",str(e))

    def sample(self):
        self.data=pd.DataFrame({"Category":["Mathematics","English","Biology","Physics"],
                                "Value":[68,74,66,82],"Study_Hours":[5,6,4,7]})
        self.refresh(); self.title.delete(0,"end"); self.title.insert(0,"Sample Student Performance")
        messagebox.showinfo("Sample data","Sample dataset loaded.")

    def clear_data(self):
        self.data=pd.DataFrame({"Category":[],"Value":[]}); self.refresh()

    def numeric(self,col):
        if col not in self.data.columns: raise ValueError(f"Column '{col}' was not found.")
        s=pd.to_numeric(self.data[col],errors="coerce")
        if s.isna().any(): raise ValueError(f"Column '{col}' contains missing or non-numeric values.")
        return s

    def generate(self):
        if self.data.empty:
            messagebox.showwarning("No data","Enter data or import a CSV file first."); return
        kind=self.kind.get(); xname=self.x.get(); yname=self.y.get()
        title=self.title.get().strip() or "Statistical Data Presentation"
        try:
            fig,ax=plt.subplots(figsize=(8,4.5),dpi=100)
            if kind in ("Bar Chart","Pie Chart","Line Graph"):
                if xname not in self.data.columns: raise ValueError("Choose a valid category/X column.")
                vals=self.numeric(yname); labels=self.data[xname].astype(str).tolist()
                if len(vals)==0: raise ValueError("No usable observations.")
                if kind=="Bar Chart":
                    ax.bar(labels,vals); ax.set_xlabel(xname); ax.set_ylabel(yname)
                elif kind=="Pie Chart":
                    if (vals<0).any() or vals.sum()<=0: raise ValueError("Pie charts need non-negative values with a positive total.")
                    ax.pie(vals,labels=labels,autopct="%1.1f%%",startangle=90); ax.axis("equal")
                else:
                    ax.plot(labels,vals,marker="o"); ax.set_xlabel(xname); ax.set_ylabel(yname)
            elif kind=="Histogram":
                vals=self.numeric(yname); ax.hist(vals,bins="auto",edgecolor="black")
                ax.set_xlabel(yname); ax.set_ylabel("Frequency")
            elif kind=="Scatter Plot":
                if xname==yname: raise ValueError("Select two different numeric columns for a scatter plot.")
                xv=self.numeric(xname); yv=self.numeric(yname)
                if len(xv)<2 or len(xv)!=len(yv): raise ValueError("Scatter plot requires at least two paired observations.")
                ax.scatter(xv,yv); ax.set_xlabel(xname); ax.set_ylabel(yname)
            ax.set_title(title)
            if kind!="Pie Chart": ax.tick_params(axis="x",labelrotation=25)
            fig.tight_layout()
            self.clear_chart()
            self.fig=fig; self.canvas=FigureCanvasTkAgg(fig,master=self.area)
            self.canvas.draw(); self.canvas.get_tk_widget().pack(fill="both",expand=True)
            self.plot_status.config(text=f"Generated {kind} using {len(self.data)} row(s).")
        except Exception as e:
            plt.close("all"); messagebox.showerror("Chart error",str(e))
            self.plot_status.config(text="Chart not generated. Check the data and settings.")

    def save(self):
        if self.fig is None:
            messagebox.showwarning("No chart","Generate a chart before saving."); return
        path=filedialog.asksaveasfilename(defaultextension=".png",
            filetypes=[("PNG image","*.png"),("PDF document","*.pdf")])
        if not path: return
        try:
            self.fig.savefig(path,bbox_inches="tight")
            messagebox.showinfo("Saved",f"Chart saved to:\n{path}")
        except Exception as e: messagebox.showerror("Save failed",str(e))

    def clear_chart(self):
        for w in self.area.winfo_children(): w.destroy()
        if self.fig is not None: plt.close(self.fig)
        self.fig=None; self.canvas=None
        self.plot_status.config(text="Choose a chart type and generate a chart.")

if __name__=="__main__":
    root=tk.Tk()
    app=ChartingApp(root)
    root.mainloop()

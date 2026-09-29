import os, tkinter as tk
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# DATA
file = os.path.join(os.path.dirname(__file__), "real_estate_dataset.csv")
df = pd.read_csv(file)
df["Date"] = pd.to_datetime(df["Date"])

total = np.sum(df.Price_Lakh)
avg = np.mean(df.Price_Lakh)
top_loc = df.groupby("Location").Price_Lakh.sum().idxmax()
top_type = df.Property_Type.value_counts().idxmax()

loc = df.groupby("Location").Price_Lakh.sum().sort_values(ascending=False)
month = df.groupby(df.Date.dt.month).Price_Lakh.sum()
ptype = df.Property_Type.value_counts()

bins = [0,100,200,300,500,np.inf]
labels = ["<100L","100-200L","200-300L","300-500L","500L+"]
price = pd.cut(df.Price_Lakh,bins,labels=labels).value_counts().sort_index()

# BeautifulSoup
soup = BeautifulSoup("<div>Mumbai</div><div>Pune</div><div>Thane</div>","html.parser")
web_data = [x.text for x in soup.find_all("div")]

# WINDOW + BIG BORDER
root = tk.Tk()
root.title("Real Estate Analytics Dashboard")
root.geometry("1400x900")
root.configure(bg="#080c14")

border = tk.Frame(root,bg="#080c14",
                  highlightbackground="#4f8cff",
                  highlightthickness=2)
border.pack(fill="both",expand=True,padx=10,pady=10)

# HEADER
tk.Label(border,text="REAL ESTATE ANALYTICS",
         font=("Segoe UI",25,"bold"),fg="white",
         bg="#080c14").pack(anchor="w",padx=35,pady=(18,0))

tk.Label(border,text="Property Market • Analytics Overview",
         font=("Segoe UI",10),fg="#8b96a8",
         bg="#080c14").pack(anchor="w",padx=37)

tk.Label(border,text="● LIVE  |  "+datetime.now().strftime("%d %b %Y  %H:%M"),
         font=("Segoe UI",9,"bold"),fg="#22c55e",
         bg="#080c14").place(relx=.82,y=25)

# KPI CARDS
cards = tk.Frame(border,bg="#080c14")
cards.pack(fill="x",padx=30,pady=18)

data = [
    ("TOTAL VALUE",f"₹{total:,.0f} L"),
    ("AVERAGE PRICE",f"₹{avg:,.1f} L"),
    ("TOTAL LISTINGS",len(df)),
    ("TOP LOCATION",top_loc),
    ("TOP PROPERTY",top_type)
]

for title,value in data:
    box=tk.Frame(cards,bg="#171c29",
                 highlightbackground="#30394d",
                 highlightthickness=1)
    box.pack(side="left",fill="both",expand=True,padx=5,ipady=10)
    tk.Label(box,text=title,font=("Segoe UI",8,"bold"),
             fg="#8793a5",bg="#171c29").pack(anchor="w",padx=14)
    tk.Label(box,text=value,font=("Segoe UI",15,"bold"),
             fg="white",bg="#171c29").pack(anchor="w",padx=14,pady=5)
    tk.Label(box,text="● Updated",font=("Segoe UI",7),
             fg="#22c55e",bg="#171c29").pack(anchor="w",padx=14)

# CHARTS
fig,ax=plt.subplots(2,2,figsize=(13,6))
fig.patch.set_facecolor("#080c14")
sns.set_theme(style="darkgrid")

sns.barplot(x=loc.index,y=loc.values,ax=ax[0,0],color="#4f8cff")
ax[0,0].set_title("PROPERTY VALUE BY LOCATION",
                  color="white",loc="left",fontweight="bold")

for i,v in enumerate(loc.values):
    ax[0,0].text(i,v/2,f"₹{v:,.0f}L",
                 ha="center",color="white",fontweight="bold")

ax[0,1].plot(month.index,month.values,
             color="#22c7d9",marker="o",linewidth=2.5)
ax[0,1].fill_between(month.index,month.values,
                     color="#22c7d9",alpha=.12)
ax[0,1].set_title("PROPERTY VALUE TREND",
                  color="white",loc="left",fontweight="bold")

ax[1,0].pie(ptype.values,labels=ptype.index,
            autopct="%1.0f%%",textprops={"color":"white"},
            wedgeprops={"width":.42,"edgecolor":"#080c14"})
ax[1,0].set_title("PROPERTY TYPE MIX",
                  color="white",loc="left",fontweight="bold")

sns.barplot(x=price.index,y=price.values,
            ax=ax[1,1],color="#8b6cff")
ax[1,1].set_title("PRICE RANGE ANALYSIS",
                  color="white",loc="left",fontweight="bold")

for i,v in enumerate(price.values):
    ax[1,1].text(i,v/2,str(v),
                 ha="center",color="white",fontweight="bold")

# CHART STYLE
for a in ax.flat:
    a.set_facecolor("#151a26")
    a.tick_params(colors="#aeb8c8",labelsize=7)
    a.set(xlabel="",ylabel="")
    a.grid(alpha=.08)
    for s in a.spines.values():
        s.set_color("#39445a")

plt.tight_layout(pad=2)

canvas=FigureCanvasTkAgg(fig,border)
canvas.draw()
canvas.get_tk_widget().pack(fill="both",expand=True,padx=28)

# INSIGHTS + FOOTER
tk.Label(border,
         text=f"KEY INSIGHTS  •  {top_loc} has highest value  •  "
              f"{top_type} is most common  •  {len(df)} properties analysed",
         font=("Segoe UI",9,"bold"),fg="#e5eaf2",
         bg="#171c29",pady=10).pack(fill="x",padx=30,pady=8)

tk.Label(border,
         text="NumPy • Pandas • Matplotlib • Seaborn • BeautifulSoup  |  Made by Amit Umar",
         font=("Segoe UI",8),fg="#718096",
         bg="#080c14").pack(pady=(0,8))

root.mainloop()

import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()
root.geometry("400x200")

def graph():
    house_prices = np.random.normal(200000, 25000, 5000)
    
    plt.hist(house_prices, 50)
    plt.show()

btn = tk.Button(root)
btn.config(text = "Graph", command = graph)
btn.pack()


root.mainloop()
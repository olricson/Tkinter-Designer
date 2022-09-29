import tkinter as tk
from tkinter import Event, EventType, filedialog

from build.gui import *

progress_1.set(0)
cnt = 0
text_id = None
curr_pos = 0

def new_bind():
    global cnt, text_id
    cnt += 1
    print(f"cnt: {cnt}")
    # entry_log.configure(text=f"{entry_log.text}\nCLICK {cnt}")
    # entry_log.configure(state=NORMAL)
    # entry_log.insert(END, f"CLICK {cnt}CLICK {cnt}CLICK {cnt}CLICK {cnt}vCLICK {cnt}CLICK {cnt}CLICK {cnt}CLICK {cnt}CLICK {cnt}CLICK {cnt}\n")
    # entry_log.configure(state=DISABLED)
    text = ""
    if text_id is not None:
        text = canvas1.itemcget(text_id, "text")
        canvas1.delete(text_id)


    text_id = canvas1.create_text(
        30,
        5,
        text=f"{text}\nCLICK {cnt}",
        anchor="nw"
    )
    progress_1.step()
    itm = canvas1.itemcget(text_id, "text")
    print(canvas1.bbox(text_id))
    # entry_log.configure(text=f"{entry_log}\nTOTO", compound="center")

def on_scroll(event):
    print(event)
    global curr_pos, text_id

    if text_id is None:
        return

    print(f'current pos: {curr_pos}')
    bbox = canvas1.bbox(text_id)
    print(f'bbox: {bbox}')
    print(f'height: {bbox[3] - bbox[1]}')

    text_height = bbox[3] - bbox[1]

    if text_height < canvas1.winfo_height():
        return


    curr_pos -= event.delta
    curr_pos = curr_pos if curr_pos > 0 else 0

    curr_pos = curr_pos if curr_pos < text_height - canvas1.winfo_height() + 30 else text_height - canvas1.winfo_height() + 30
    text = canvas1.itemcget(text_id, "text")
    canvas1.delete(text_id)

    text_id = canvas1.create_text(
        30,
        5-curr_pos,
        text=text,
        anchor="nw"
    )

def hover(event: Event):
    if event.type == EventType.Enter:
        event.widget.master.configure(
            border_width=2,
            border_color="#952866",
        )
    elif event.type == EventType.Leave:
        event.widget.master.configure(
            border_width=0
        )

def select_csv(event):
    output_path = filedialog.askopenfilename(filetypes=[("CSV files", ".csv")])
    entry_csv.delete(0, END)
    entry_csv.insert(0, output_path)

def select_observable(event):
    output_path = filedialog.askopenfilename(filetypes=[("TXT files", ".txt")])
    entry_observable.delete(0, END)
    entry_observable.insert(0, output_path)

def select_output(event):
    output_path = filedialog.askdirectory()
    entry_output.delete(0, END)
    entry_output.insert(0, output_path)

entry_sit.bind("<Enter>", func=hover)
entry_sit.bind("<Leave>", func=hover)
entry_csv.bind("<Enter>", func=hover)
entry_csv.bind("<Leave>", func=hover)
entry_user.bind("<Enter>", func=hover)
entry_user.bind("<Leave>", func=hover)
entry_observable.bind("<Enter>", func=hover)
entry_observable.bind("<Leave>", func=hover)
entry_output.bind("<Enter>", func=hover)
entry_output.bind("<Leave>", func=hover)

entry_csv.bind("<Button-1>", func=select_csv)
entry_observable.bind("<Button-1>", func=select_observable)
entry_output.bind("<Button-1>", func=select_output)

button_generate.configure(command=new_bind)

combobox_1.configure(text_color="#FFFFFF", values=["P6X"])
combobox_1.set("P6X")

canvas1.bind("<MouseWheel>", on_scroll)

# entry_log.configure(state=DISABLED)

window.title("CESIMA")

window.resizable(False, True)
window.mainloop()

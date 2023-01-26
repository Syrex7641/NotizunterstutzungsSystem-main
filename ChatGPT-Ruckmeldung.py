import os
import openai
import tkinter as tk
from tkinter import ttk

string = "test"
api_key = "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"
bedingungen = "Vorgabe: 250 Zeichen, auf Deutsch kurz und prägnant."

def send_request(prompt_suffix, engine):
    input_text = input_field.get()
    openai.api_key = api_key
    prompt = f"{prompt_suffix} {input_text}"
    completions = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    )

    message = completions.choices[0].text
    history.append("------------------------")
    history.append(f"Anfrage: {input_text}\n")
    history.append("- - - - - - - - - - - -")
    history.append(f"Antwort: {message}\n")
    history.append("\n\n")
    output_field.configure(state='normal')
    output_field.delete(1.0,tk.END)
    output_field.insert(tk.INSERT, message)
    output_field.configure(state='normal')

def send_request_window(engine, question, output_field_window, window):
    input_text = input_field.get()
    openai.api_key = api_key
    prompt = f"{question} im bezug auf {input_text}"
    completions = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    )
    message = completions.choices[0].text
    history.append("------------------------")
    history.append(f"Anfrage: {question}\n")
    history.append("- - - - - - - - - - - -")
    history.append(f"Antwort: {message}\n")
    history.append("\n\n")
    output_field_window.configure(state='normal')
    output_field_window.delete(1.0,tk.END)
    output_field_window.insert(tk.INSERT, "Frage: "+question)
    output_field_window.insert(tk.INSERT, "\n- - - - - - - - - - - -\n")
    output_field_window.insert(tk.INSERT, message)
    output_field_window.insert(tk.INSERT, "\n------------------------\n")
    output_field_window.configure(state='normal')
    window.update()

def return_todo():
    send_request("Schreib mir eine Schritt für Schritt Anleitung für ", engine)

def return_antwort(input_field_window, output_field_window, window):
    send_request_window(engine, input_field_window, output_field_window, window)

def return_feedback():
    send_request("Bewerte mein Vorhaben und nenn mir dazu jeweils 3 Vor- und Nachteile. Mein Vorhaben lautet:", engine)

def return_prices():
    send_request("Erstelle einen tabelarisch aufgebauten Kostenplan für folgendes Vorhaben:", engine)

def return_context():
    send_request("Ich habe eine frage zu meinem Vorhaben:", engine)

def save_history():
    if not os.path.exists("responses.txt"): open("responses.txt","w").close()
    with open("responses.txt","w") as f:
        for i in history:
            f.write(i + "\n")
            f.flush()
            os.fsync(f.fileno())
        f.close()

def open_window():
    window = tk.Toplevel(root)
    window.title("Antworten!")
    root_geometry = root.winfo_geometry()
    window_width = int(root_geometry.split("x")[0])
    window.geometry(f"+{window_width}+0")
    input_label_window = ttk.Label(window, text="Deine Frage:")
    input_label_window.grid(column=0,row=0)
    output_field_window = tk.Text(window)
    output_field_window.grid(column=1, row=1)
    output_field_window.configure(state='disabled')
    input_field_window = ttk.Entry(window)
    input_field_window.grid(column=1, row=0)
    input_field_window.bind("<Return>", lambda event: return_antwort(input_field_window.get(),output_field_window,window))

def change_engine():
    selected_engine = comboengine.get()
    global engine
    case = {
        "Davinci 3": "text-davinci-003",
        "Davinci 2": "text-davinci-002",
        "Davinci 1": "text-davinci-001",
        "Curie 1":"text-curie-001",
        "Babbage 1":"text-babbage-001"
    }
    engine = case.get(selected_engine)
    return engine

history = []
enginelist = ["Davinci 3","Davinci 2","Davinci 1","Curie 1","Babbage 1"]

root = tk.Tk()
root.title("Notizen ChatGPT")

input_label = ttk.Label(root, text="Dein Vorhaben:")
input_label.grid(column=0,row=0)

input_field = ttk.Label(root)
input_field.grid(column=1, row=0)

input_field = ttk.Entry(root)
input_field.grid(column=1, row=0)
input_field.bind("<Return>", lambda event: return_todo())

comboengine = ttk.Combobox(root, values = enginelist)
comboengine.set("Davinci 3")
comboengine.grid(column=2, row=0)
comboengine.bind(lambda event: change_engine())


button = tk.Button(root, text="Senden",command=return_todo)
button.grid(column=1, row=2)

button = tk.Button(root, text="Speichern", command=save_history)
button.grid(column=2,row=1)

button = tk.Button(root, text="Feedback",command=return_feedback)
button.grid(column=1,row=3)

button = tk.Button(root, text="Kostenvoranschlag", command=return_prices)
button.grid(column=1,row=4)

output_label = tk.Label(root,text="Antwort:")
output_label.grid(column=0, row=1)

button = tk.Button(root, text="Bei Fragen, fragen", command=open_window)
button.grid(column=0,row=2)

output_field = tk.Text(root)
output_field.grid(column=1, row=1)
output_field.configure(state='disabled')

engine = change_engine()
root.mainloop()

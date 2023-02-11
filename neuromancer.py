import hashlib
import json, sys
import tkinter as tk
from tkinter import filedialog

class Neuromancer:
    def __init__(self, filename, tolerance=10):
        self.filename = filename
        self.file_hash = ""
        self.tolerance = tolerance

    def check_tolerance(self, score):
        if score >= self.tolerance:
            return True
        else:
            return False

    def get_similarity(self, score):
        return round((score / 128) * 100, 2)

    def compare(self, sign_a, sign_b):
        score = 0
        for i in range(128):
            if sign_a[i] == sign_b[i]:
                score += 1
        return score

    def first_check(self, sign_a, sign_b):
        if sign_a == sign_b:
            return True
        else:
            return False

    def hash_file(self):
        try:
            with open(self.filename, "rb") as fl:
                data = fl.read()
            self.file_hash = hashlib.blake2b(data).hexdigest()
        except Exception as error:
            print(error)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        self.create_widgets()
        self.configure(background='white')

    def create_widgets(self):
        self.browse_button = tk.Button(self, text="Iniciar varredura", font=("Helvetica", 14), bg="#0f0f0f",
                                       fg="#ffffff", activebackground="#1f1f1f", activeforeground="#ffffff",
                                       command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Courier", 16), width=25, height=2)
        self.result_label.pack(pady=10)

        self.quit = tk.Button(self, text="Desistir", font=("Helvetica", 14), bg="#0f0f0f", fg="#ffffff",
                              activebackground="#1f1f1f", activeforeground="#ffffff", command=root.destroy)
        self.quit.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        neuro = Neuromancer(file_path)
        neuro.hash_file()

        fl = open("sigs.json")
        signatures = json.load(fl)
        fl.close()

        for key in signatures.keys():
            if neuro.first_check(neuro.file_hash, signatures[key]):
                self.result_label.config(text="[+] Amostra encontrada: " + key, fg="#00FF00")
                break
            score = neuro.compare(neuro.file_hash, signatures[key])
            percent = neuro.get_similarity(score)
            if neuro.check_tolerance(percent):
                self.result_label = tk.Label(self, text="[?] Possível amostra encontrada: " + key + " [" + str(
                    percent) + "%]", fg="#FFFF00")
            self.result_label.pack(side="bottom")
        else:
            self.result_label = tk.Label(self, text="[-] Nenhuma amostra encontrada", fg="#FF0000")
            self.result_label.pack(side="bottom")

        file_path = filedialog.askopenfilename()
        neuro = Neuromancer(file_path)
        neuro.hash_file()

        fl = open("sigs.json")
        signatures = json.load(fl)
        fl.close()

        for key in signatures.keys():
            if neuro.first_check(neuro.file_hash, signatures[key]):
                self.result_label.config(text="[+] Amostra encontrada: " + key, fg="#00FF00")
                break
            score = neuro.compare(neuro.file_hash, signatures[key])
            percent = neuro.get_similarity(score)
            if neuro.check_tolerance(percent):
                self.result_label = tk.Label(self, text="[?] Possível amostra encontrada: " + key + " [" + str(
                    percent) + "%]", fg="#FFFF00")
            self.result_label.pack(side="bottom")
            break
        else:
            self.result_label = tk.Label(self, text="[-] Nenhuma amostra encontrada", fg="#FF0000")
            self.result_label.pack(side="bottom")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

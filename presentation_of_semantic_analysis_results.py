import requests
import json

import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *

import os
from docx import Document
import nltk

file_name = []
file_name.append('')

def get_filename():
    global file_name
    file_name[0] = filedialog.askopenfilename(filetypes=(("Документ Microsoft Word", "*.docx"),))
    word.insert(0, file_name[0])


def synonyms(word):
    res = requests.get(f"http://api.conceptnet.io/query?start=/c/ru/{word}&rel=/r/Synonym")
    parsed = json.loads(res.content)

    syns = []
    for edge in parsed['edges']:
        syns.append(edge['end']['label'])
    return syns

def build_graph(syns, new_word,i):
    edges = [(new_word, syn) for syn in syns]

    G=nx.Graph()
    G.add_edges_from(edges)

    nx.draw(G)
    nx.draw_networkx_labels(G, pos=nx.spring_layout(G))
    print(os.getcwd())
    plt.savefig(os.getcwd() + "\graph" + str(i) + ".png")

def click():
    path = word.get().replace('\n', '')
    document = Document(path)
    document.save(path)

    message = ""
    for para in document.paragraphs:
        message += para.text
    message = message.replace('\n', '')
    message = message.replace(',', '')
    message = message.replace(':', '')
    message = message.replace('!', '')
    message = message.replace('?', '')
    message = message.replace('.', '')

    if message != '':
        nltk.download('punkt')
        doc = nltk.word_tokenize(message)
        print(doc)
        i = 0
        for text in doc: 
            print(text)
            syns = synonyms(text)
            build_graph(syns, text,i)
            i += 1
def info():
    messagebox.askquestion("Help", "1. Нажмите Открыть файл.\n"
                                   "2. Выберите doc файл с предложением\n"
                                   "3. Нажмите кнопку 'Ok'.\n", type='ok')

window = Tk()
window.title("Synonyms")

open_file_btn = Button(text="Открыть файл", command=get_filename)
open_file_btn.grid(row=0, column=0)

Label(window, text="Input word:").grid(column=1, row=0)

word = Entry(window,width=20)
word.grid(column=2, row=0)

btn = Button(window, text="Get tree", command=click)
btn.grid(column=3, row=0)
Button(text="info?", width=10, command=info).grid(row=0,column=4)

window.mainloop()

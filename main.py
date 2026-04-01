import spacy
import networkx as nx
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')

with open(r"d:\Coding\knowledge graph\text.txt", "r") as file:
    text = file.read().strip()

if not text:
    raise ValueError("Input file is empty")

doc = nlp(text)

triples = []

for sent in doc.sents:
    subject = None
    relation = None
    obj = None

    for token in sent:
        if "subj" in token.dep_:
            subject = token.text
        elif token.pos_ == "VERB":
            relation = token.text
        elif "obj" in token.dep_:
            obj = token.text

    if subject and relation and obj:
        triples.append((subject, relation, obj))

if not triples:
    raise ValueError("No valid relationships found in text")

G = nx.DiGraph()

for subj, rel, obj in triples:
    G.add_edge(subj, obj, label=rel)

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000)

edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.savefig("graph.png")
plt.show()
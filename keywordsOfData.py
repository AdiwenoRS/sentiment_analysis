# def pisahkan_kata(kalimat):
#     return kalimat.split()

# kalimat = "Ini adalah contoh kalimat"
# hasil = pisahkan_kata(kalimat)
# print(hasil)

def keywords(filtered_sentences):
    for obj, sentence in filtered_sentences.items():
        for sentence in sentence:
            filtered_sentences[obj] = [sentence.split()]
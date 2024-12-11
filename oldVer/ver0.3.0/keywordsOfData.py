def keywords(filtered_sentences, splittedSentences):
    for obj, sentence in filtered_sentences.items():
        splittedSentences[obj] = [] # Add empty lists
        for sentence in sentence:
            split_value = sentence.split()
            splittedSentences[obj].append(split_value)

def deleteSomeWords(wordsToDelete, splittedSentences):
    for obj, sentences in splittedSentences.items():
        for sentence in sentences:
            for word in wordsToDelete:
                if word in sentence:
                    sentence.remove(word)
            

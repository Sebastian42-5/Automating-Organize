from collections import Counter 

paragraph = input('Enter your paragraph: ').split()

characters = ' '.join(paragraph)

number_of_characters = len(characters)

number_of_sentences = characters.count('.') + characters.count('?') + characters.count('!')

number_of_words = len(paragraph)

most_common_words = Counter(paragraph)

most_common_word = most_common_words.most_common()[0][0]

print(f'\nYour paragraph has {number_of_words} words, {number_of_sentences} sentences, and {number_of_characters} characters! The most common word is : {most_common_word}')







import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
from translate import Translator

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')
# Инициализация инструмента
translator = Translator(to_lang="en")

# Шаг 1: Чтение текста из файла
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Шаг 2: Нормализация слов (лемматизация)
def normalize_words(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    normalized_words = [
        lemmatizer.lemmatize(word.lower()) for word in words
        if word.isalpha() and word.lower() not in stop_words
    ]
    return normalized_words

# Шаг 3: Подсчет частоты слов
def count_words(words):
    return Counter(words)

# Шаг 4: Перевод слов на английский язык
def translate_words(word_counts):
    translated_dict = {}
    for word, count in word_counts.items():
        try:
            translated_word = translator.translate(word)
            translated_dict[translated_word] = count
        except Exception as e:
            print(f"Ошибка при переводе слова '{word}': {e}")
            translated_dict[word] = count
    return translated_dict

# Шаг 5: Сохранение результатов в файл
def save_results(word_dict, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count in word_dict.items():
            file.write(f"{word}: {count}\n")

# Основной рабочий процесс
def main(input_file, output_file):
    text = read_text(input_file)
    normalized_words = normalize_words(text)
    word_counts = count_words(normalized_words)
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda x: -x[1]))
    translated_word_counts = translate_words(sorted_word_counts)
    save_results(translated_word_counts, output_file)
    print(f"Результаты сохранены в {output_file}")

# Замените на ваши пути к файлам
input_file_path = 'chat.txt'  # Путь к входному текстовому файлу
output_file_path = 'output_results.txt'  # Путь для сохранения результатов

main(input_file_path, output_file_path)

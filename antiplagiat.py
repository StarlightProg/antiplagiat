import re
import hashlib

def preprocess_text(text):
    """Нормализует текст: удаляет знаки препинания, приводит к нижнему регистру"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Убираем пунктуацию
    return text

def get_shingles(text, k=5):
    """Разбивает текст на шинглы длиной k символов и хеширует их"""
    text = preprocess_text(text)
    shingles = {hashlib.md5(text[i:i + k].encode()).hexdigest() for i in range(len(text) - k + 1)}
    return shingles

def jaccard_similarity(set1, set2):
    """Вычисляет коэффициент Жаккара"""
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0

def check_plagiarism(text1, text2, k=5, threshold=0.3):
    """Проверяет схожесть двух текстов"""
    shingles1 = get_shingles(text1, k)
    shingles2 = get_shingles(text2, k)
    similarity = jaccard_similarity(shingles1, shingles2)
    return similarity, similarity >= threshold

def read_file(filepath):
    """Считывает текст из файла"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    file1 = "text1.txt"  # Укажите путь к первому файлу
    file2 = "text2.txt"  # Укажите путь ко второму файлу
    
    text1 = read_file(file1)
    text2 = read_file(file2)
    
    similarity, is_plagiarized = check_plagiarism(text1, text2)
    print(f"Коэффициент схожести: {similarity:.2f}")
    print("Текст заимствован" if is_plagiarized else "Текст оригинальный")

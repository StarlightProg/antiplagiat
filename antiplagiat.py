import os
import docx
from difflib import SequenceMatcher

def read_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def read_doc_file(filepath):
    doc = docx.Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_document(filepath):
    if filepath.endswith('.txt'):
        return read_txt_file(filepath)
    elif filepath.endswith('.doc') or filepath.endswith('.docx'):
        return read_doc_file(filepath)
    else:
        return ''

def get_documents_from_folder(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt') or filename.endswith('.doc') or filename.endswith('.docx'):
            full_path = os.path.join(folder_path, filename)
            content = read_document(full_path)
            documents[filename] = content
    return documents

def compare_texts(text1, text2):
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio()

def analyze_original_for_plagiarism(documents, original_filename='original.txt'):
    if original_filename not in documents:
        print(f"Файл {original_filename} не найден.")
        return {}

    original_text = documents[original_filename]
    max_similarity = 0.0
    source_document = None
    similarities = {}

    for filename, text in documents.items():
        if filename == original_filename:
            continue
        similarity = compare_texts(original_text, text)
        similarities[filename] = similarity
        if similarity > max_similarity:
            max_similarity = similarity
            source_document = filename

    originality = 1 - max_similarity

    result = {
        'Процент оригинальности original.txt': round(originality * 100, 2),
        'Наибольшее совпадение с': source_document,
        'Процент совпадения': round(max_similarity * 100, 2),
        'Подробности': {doc: round(sim * 100, 2) for doc, sim in similarities.items()}
    }

    return result

def save_report(result, output_file='plagiarism_report.txt'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'Проверка документа: original.txt\n')
        f.write(f'Оригинальность: {result["Процент оригинальности original.txt"]}%\n')
        f.write(f'Наибольшее совпадение с: {result["Наибольшее совпадение с"]}\n')
        f.write(f'Процент совпадения: {result["Процент совпадения"]}%\n')
        f.write('\nДетальное сравнение с каждым документом:\n')
        for doc, percent in result['Подробности'].items():
            f.write(f'- {doc}: {percent}% совпадения\n')

def main():
    folder_path = input("Введите путь к папке с документами: ")
    documents = get_documents_from_folder(folder_path)
    result = analyze_original_for_plagiarism(documents, original_filename='original.txt')

    print(f"\nПроверка original.txt на заимствование:")
    print(f'Оригинальность: {result["Процент оригинальности original.txt"]}%')
    print(f'Наибольшее совпадение с: {result["Наибольшее совпадение с"]}')
    print(f'Процент совпадения: {result["Процент совпадения"]}%\n')

    print("Детальное сравнение:")
    for doc, percent in result['Подробности'].items():
        print(f'- {doc}: {percent}%')

    save_report(result)
    print("\nОтчет сохранен в файл plagiarism_report.txt")

if __name__ == '__main__':
    main()

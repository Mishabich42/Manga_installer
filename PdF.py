from reportlab.pdfgen import canvas
from PIL import Image
import os
name = "Історія виживання короля меча у іншому світі"
def create_pdf(name):
    # Шлях до папки із завантаженими зображеннями
    image_folder = name

    # Список імен зображень у папці
    image_files = os.listdir(image_folder)

    # Сортуємо зображення за назвою у правильному порядку
    image_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    # Шлях до вихідного PDF-файлу
    pdf_file = f'{name}.pdf'

    # Створюємо новий PDF-файл
    c = canvas.Canvas(pdf_file)

    # Додаємо кожне зображення до PDF
    for image_file in image_files:
        try:
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path)
            pdf_width, pdf_height = img.size  # Розмір PDF-сторінки відповідає розміру зображення
            c.setPageSize((pdf_width, pdf_height))  # Встановлюємо розмір сторінки
            c.drawImage(image_path, 0, 0, pdf_width, pdf_height)  # Додаємо зображення
            c.showPage()  # Додаємо нову сторінку
        except Exception:
            print(image_file)
            c.save()
    c.save()

    print(f'PDF файл "{pdf_file}" створено успішно.')
create_pdf(name)
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from time import sleep
from requests import get
from reportlab.pdfgen import canvas
from PIL import Image as PilImage

url = 'https://honey-manga.com.ua'


def download_images(name_manga, select_page):
    # Create a PDF file
    pdf_file = f'{name_manga}.pdf'
    c = canvas.Canvas(pdf_file, pagesize=letter)
    # Initialize the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Activate headless mode
    driver = webdriver.Chrome(options=options)

    # Navigate to the webpage
    driver.get(url)
    sleep(0.3)
    Button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/div[2]/button"))
    )
    Button[0].click()
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
    )
    search[0].send_keys(name_manga)
    sleep(2)
    Button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > div.MuiDialog-root.MuiModal-root.css-1d6jd40 > div.MuiDialog-container.MuiDialog-scrollPaper.css-ekeie0 > div > div > div.mt-6.MuiBox-root.css-10d4j3m > button:nth-child(1) > div:nth-child(1) > div > span"))
    )
    Button[0].click()
    sleep(1)
    Button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__next"]/div/div[3]/div[1]/div[2]/div[2]/a'))
    )
    Button[0].click()
    while True:
        sleep(0.5)
        Page = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/button[2]'))
        )
        Page = Page[0].text
        print(Page)
        if len(Page.split("-")) > 1 and Page.split("-", 1)[1].strip() == select_page:
            print("Go")
            break
        else:
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                '#__next > div.flex.flex-col.min-h-full > div.MuiBox-root.css-1g0x2vd > div > div > div > div.col-span-8.lg\:col-span-4.flex.justify-center > div > button:nth-child(3)'))
                )
                button.click()
            except Exception:
                # If the "Next" button is not found, exit the loop
                print("Session ended")
                break
    while True:
        # Get all images on the page
        sleep(3)
        images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )

        # Download and add images to the PDF
        for img in images:
            img_url = img.get_attribute('src')
            if img_url:
                try:
                    response = get(img_url)
                    img_data = BytesIO(response.content)
                    pil_image = PilImage.open(img_data)
                    img_width, img_height = pil_image.size
                    pdf_width, pdf_height = img_width, img_height  # Set PDF page size based on image size
                    c.setPageSize((pdf_width, pdf_height))  # Set the PDF page size
                    c.drawImage(ImageReader(img_data), 0, 0, pdf_width, pdf_height)  # Add image to PDF
                    c.showPage()  # Add a new page to the PDF
                except Exception as e:
                    print(f"Error adding image to PDF: {e}")
        # Get the "Next" button and click it
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#__next > div.flex.flex-col.min-h-full > div.MuiBox-root.css-1g0x2vd > div > div > div > div.col-span-8.lg\:col-span-4.flex.justify-center > div > button:nth-child(3)'))
            )
            button.click()
        except Exception:
            # If the "Next" button is not found, exit the loop
            print("Session ended")
            break
    c.save()
    # Quit the webdriver
    driver.quit()

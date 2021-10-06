# python -m pytest -v --driver Chrome --driver-path D:/chrome_driver/chromedriver.exe test_my_pets.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets(web_browser):
    """Проверяем загрузку страницы my_pets."""
    WebDriverWait(web_browser, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'h2')))
    page_load = web_browser.find_element_by_tag_name('h2')
    assert page_load.is_displayed(), "WARNING my pets are not visible"


def test_show_all_my_pets(web_browser):
    """Проверяем присутствие всех питомцев на странице."""
    WebDriverWait(web_browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//body/div[1]/div/div[1]')))
    number_of_pets = int(web_browser.find_element_by_xpath('//body/div[1]/div/div[1]').text.split()[2])
    WebDriverWait(web_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr')))
    number_of_table_rows = len(web_browser.find_elements_by_xpath('//table/tbody/tr'))

    assert number_of_pets == number_of_table_rows, "WARNING not all pets are displayed"


def test_half_pets_have_photo(web_browser):
    """Проверяем наличие фото хотя бы у половины питомцев."""
    WebDriverWait(web_browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//body/div[1]/div/div[1]')))
    number_of_pets = int(web_browser.find_element_by_xpath('//body/div[1]/div/div[1]').text.split()[2])
    WebDriverWait(web_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//img[@src=""]')))
    number_of_pets_without_photo = len(web_browser.find_elements_by_xpath('//img[@src=""]'))

    assert (number_of_pets / 2) >= number_of_pets_without_photo, "WARNING the number of pets without " \
                                                                 "a photo is more than 50%"


def test_all_pets_have_name(web_browser):
    """Проверяем наличие имени у всех питомцев."""
    WebDriverWait(web_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr/td[1]')))
    names = web_browser.find_elements_by_xpath('//table/tbody/tr/td[1]')

    for pet in range(len(names)):
        assert names[pet].text != '', "WARNING not all pets have a name"


def test_all_pets_have_breed(web_browser):
    """Проверяем наличие породы у всех питомцев."""
    WebDriverWait(web_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr/td[2]')))
    breeds = web_browser.find_elements_by_xpath('//table/tbody/tr/td[2]')

    for pet in range(len(breeds)):
        assert breeds[pet].text != '', "WARNING not all pets have a breed"


def test_all_pets_have_age(web_browser):
    """Проверяем наличие возраста у всех питомцев."""
    WebDriverWait(web_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr/td[3]')))
    ages = web_browser.find_elements_by_xpath('//table/tbody/tr/td[3]')

    for pet in range(len(ages)):
        assert ages[pet].text != '', "WARNING not all pets have age"


def test_duplicate_pet_names(web_browser):
    """Проверяем отсутствие дубликатов имен у питомцев."""
    WebDriverWait(web_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr/td[1]')))
    names = web_browser.find_elements_by_xpath('//table/tbody/tr/td[1]')

    # Задаем пустой список
    data_names = []

    # Добавляем имена в список
    for name in names:
        name = name.text
        data_names.append(name)

    # Задаем счетчики item_name - для задания цикла перебора имен в списке и k - для подсчета дубликатов имен питомцев
    item_name = 0
    k = 0
    # Проверяем список на наличие дубликат имен
    while item_name < len(data_names) - 1:
        if data_names[item_name] == data_names[item_name + 1]:
            k += 1

        item_name += 1

    assert k == 0, "WARNING pets have duplicate names"


def test_duplicate_pets(web_browser):
    """Проверяем отсутствие дубликата питомцев."""
    # Создаем пустой список и счетчик
    data_pets = []
    k = 1

    # Загружаем страницу
    WebDriverWait(web_browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//body/div[1]/div/div[1]')))
    number_of_pets = int(web_browser.find_element_by_xpath('//body/div[1]/div/div[1]').text.split()[2])

    # Ждем загрузку всех строк таблицы
    WebDriverWait(web_browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//table/tbody/tr')))

    # Находим имя, породу и возраст всех питомцев
    while k <= number_of_pets:
        name = web_browser.find_element_by_xpath(f'//table/tbody/tr[{k}]/td[1]').text
        breed = web_browser.find_element_by_xpath(f'//table/tbody/tr[{k}]/td[2]').text
        age = web_browser.find_element_by_xpath(f'//table/tbody/tr[{k}]/td[3]').text

        # Собираем полученные данные в массив
        data_pets.append({
            'name': name,
            'breed': breed,
            'age': age
        })

        k += 1

    # Задаем два счетчика item - для задания цикла перебора питомцев в массиве и n - для подсчета дубликатов питомцев
    item = 0
    n = 0

    # Проверяем массив на наличие дубликатов питомцев
    while item < len(data_pets) - 1:
        if data_pets[item] == data_pets[item + 1]:
            n += 1

        item += 1

    assert n == 0, "WARNING some pets have duplicates"

"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
"""
import threading
import requests
from multiprocessing import Process, Pool
import time


urls = ['https://www.istockphoto.com/photo/portrait-of-young-'
        'smiling-woman-face-partially-covered-with'
        '-flying-hair-in-windy-day-gm1297159365-390363037/',
        'https://www.istockphoto.com/essential/photo/'
        'shot-of-a-young-family-playing-together-on-the-lounge-floor'
        '-at-home-gm1366667952-437135131',
        ]


def download(url):
    response = requests.get(url)
    filename = 'multiprocessing_' + url.replace('https://','').replace('.', '_').replace('/', '') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


processes = []
start_time = time.time()


if __name__ == '__main__':
    for url in urls:
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

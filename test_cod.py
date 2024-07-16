import aiohttp
import asyncio
import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import multiprocessing

# Функция для сохранения изображения на диск


def save_image(content, file_name):
    with open(file_name, 'wb') as f:
        f.write(content)

# Асинхронная функция для загрузки изображения


async def download_image(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                file_name = os.path.basename(urlparse(url).path)
                save_image(content, file_name)
                return url, file_name
            else:
                return url, None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return url, None

# Асинхронная функция для обработки списка URL-адресов


async def download_images(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Функция для запуска асинхронного кода в отдельном процессе


def run_async_download(urls):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(download_images(urls))
    return results


def main(urls):
    if not urls:
        print("No URLs provided. Please provide a list of image URLs to download.")
        return

    start_time = time.time()
    num_cpus = multiprocessing.cpu_count()

    # Используем ThreadPoolExecutor для многопоточности
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        future = executor.submit(run_async_download, urls)
        results = future.result()

    for url, file_name in results:
        if file_name:
            print(f"Downloaded {file_name} from {url}")
        else:
            print(f"Failed to download from {url}")

    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download images from URLs.')
    parser.add_argument('urls', nargs='*', help='List of image URLs to download')
    args = parser.parse_args()

    if not args.urls:
        parser.print_help()
    else:
        main(args.urls)

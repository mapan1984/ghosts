import asyncio
import aiohttp

from downloader.process_bar import make_process_bar


async def fetch(url, queue, loop=None):
    headers = {
        'Accept-Encoding':'*',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/53.0.2785.116 Safari/537.36',
    }
    chunk_size = 1024
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url, headers=headers) as resp:
            process_bar = make_process_bar(
                int(resp.headers.get('Content-Length'))
            )
            has_load = 0
            while True:
                chunk = await resp.content.read(chunk_size)
                if not chunk:
                    break
                has_load += len(chunk)
                process_bar(has_load)
                await queue.put(chunk)
    await queue.put(None)

async def save(filename, queue):
    with open(filename, 'wb') as fd:
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            fd.write(chunk)

HOSTS_URL = r"https://github.com/racaljk/hosts/raw/master/hosts"

def download(url, filename):
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    fetcher = fetch(url, queue, loop=loop)
    saver = save(filename, queue)
    loop.run_until_complete(asyncio.gather(fetcher, saver))
    loop.close()

if __name__ == '__main__':
    download(HOSTS_URL, 'hosts')


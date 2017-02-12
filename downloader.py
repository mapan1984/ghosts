import os
import queue
import threading
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def make_process_bar(total, init_has_load=0):
    """ 构建process_bar, 显示进度条
    argv:
        total：文件总字节数
        init_has_load：已下载字节数
    use:
        process_bar = make_process_bar(total, init_has_load=0)
        process_bar(has_load)
    """
    done_num = int(init_has_load/total * 100) 
    print("[{done_str}{empty_str}]{done_num}%".format(
            done_str=">"*done_num, empty_str=" "*(100-done_num), 
            done_num=done_num), end='\r')
    
    def process_bar(has_load):
        """ 传入has_load，显示进度 """
        nonlocal done_num
        new_done_num = int(has_load/total * 100)
        if done_num != new_done_num:
            done_num = new_done_num
            rest_num = 100 - done_num
            print("[{done_str}{empty_str}]{done_num}%".format(
                    done_str=">"*done_num, empty_str=" "*(rest_num), 
                    done_num=done_num), end='\r')
        if done_num == 100:
            print()
            
    return process_bar

class Producer(threading.Thread):
    def __init__(self, url, queue):
        super(Producer, self).__init__()
        self.url = url
        self.queue = queue

    def run(self):
        try:
            response = urlopen(self.url)
        except HTTPError as e:
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
            return None
        except URLError as e:
            print("We failed to reach a server.")
            print("Error Reason: ", e.reason)
            return None
        else:
            print("We get response.")
            print("Start download.")
            # 获取文件长度（单位Byte）
            file_length = int(response.info()['Content-length'])
            # 构造show_process_bar用于显示进度
            process_bar = make_process_bar(file_length)
            loaded_length = 0
            while True:
                content = response.read(1024)
                self.queue.put(content)
                loaded_length += len(content)
                process_bar(loaded_length)
                if len(content) == 0:
                    self.queue.put('done')
                    break
            print("Response is done.")
            response.close()

class Consumer(threading.Thread):
    def __init__(self, filename, queue):
        super(Consumer, self).__init__()
        self.filename = filename
        self.queue = queue

    def run(self):
        file = open(self.filename, "wb")
        while True:
            content = self.queue.get()
            if content == 'done':
                print("Download is done.")
                break
            file.write(content)
            self.queue.task_done()
        file.close()

HOSTS_URL = r"https://github.com/racaljk/hosts/raw/master/hosts"

def download(url, filename):
    q = queue.Queue()
    p = Producer(url, q)
    c = Consumer(filename, q)
    p.start()
    c.start()
    p.join()
    c.join()

if __name__ == '__main__':
    download(HOSTS_URL, 'hosts')

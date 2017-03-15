try:
    from downloader.async_downloader import download
except:
    from downloader.thread_downloader import download

__all__ = ['download']

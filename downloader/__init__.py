try:
    from downloader.async_downloader import download
except ImportError:
    from downloader.thread_downloader import download

__all__ = ['download']

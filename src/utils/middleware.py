import os
import psutil
import logging

logger = logging.getLogger(__name__)

THRESHOLD = 2 * 1024 * 1024


class MemoryUsageMiddleware:
    def process_request(self, request):
        request.mem = psutil.Process(os.getpid()).memory_info()

    def process_response(self, request, response):
        mem = psutil.Process(os.getpid()).memory_info()
        diff = mem.rss - request.mem.rss

        if diff > THRESHOLD:
            logger.warning('MEMORY USAGE ({url}) {mem:,d}'.format(
                url=request.path,
                mem=diff,
            ))

        return response

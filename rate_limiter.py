
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def allow_request(self, client_ip):
        now = time.time()
        if client_ip not in self.requests:
            self.requests[client_ip] = deque()
        window = self.requests[client_ip]
        while window and window[0] <= now - self.window_seconds:
            window.popleft()
        if len(window) < self.max_requests:
            window.append(now)
            return True
        return False

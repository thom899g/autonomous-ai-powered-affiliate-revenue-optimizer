import logging
from typing import Dict, Optional

class Monitor:
    def __init__(self):
        self.metrics = {}
        self.logger = logging.getLogger(__name__)
        
    def
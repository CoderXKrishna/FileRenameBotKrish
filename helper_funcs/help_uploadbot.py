#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import requests
from time import time
from humanize import intcomma, nbytes

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def DetectFileSize(url):
    r = requests.head(url, allow_redirects=True)
    total_size = int(r.headers.get("content-length", 0))
    return total_size


def DownLoadFile(url, file_name, chunk_size, client=None, ud_type=None, message_id=None, chat_id=None):
    if os.path.exists(file_name):
        os.remove(file_name)
    if not url:
        return file_name
    r = requests.get(url, allow_redirects=True, stream=True)
    total_size = int(r.headers.get("content-length", 0))
    downloaded_size = 0
    with open(file_name, 'wb') as fd:
        start_time = time()
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
                downloaded_size += chunk_size
                elapsed_time = time() - start_time
                if elapsed_time >= 0.3 and client is not None:
                    start_time = time()
                    client.edit_message_text(
                        chat_id,
                        message_id,
                        text=f"{ud_type}: {intcomma(downloaded_size)} of {nbytes(total_size)}"
                    )
    return file_name

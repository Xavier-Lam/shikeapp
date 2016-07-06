# -*- coding: utf-8 -*-

from log import init_log
from model import Session, User
from shike import ShikeClient
from tasks import run

if __name__ == "__main__":
    init_log()
    session = Session()
    users = session.query(User).all()

    for user in users:    
        client = ShikeClient(user.uid, user.key, user.idfa)
        client.init()
        run.delay(client)
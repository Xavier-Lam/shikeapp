# -*- coding: utf-8 -*-

import logging
import os
import sys

import config
from model import Session, User
from shike import ShikeClient
from tasks import run

def init():
    from model import engine, Model

    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    session = Session()

    user1 = User(name="xvl", uid="24238285", key="C3D680D6B15EEE17BCB2BF24419A8F82",
        idfa="37B9B63C-FCF7-4D47-854E-FD17D606E300", 
        openid="oFfv-s7eYZ8n7Z6buxKiMhql7ehE")
    user2 = User(name="yyc", uid="24805851", key="F84630346706B10753B0E8E6EED2DC28",
        idfa="A5AB7442-38D1-40D5-989C-D601AF6EB4D0", 
        openid="oFfv-s9Xqqr1-szHZU9eIaVBZzy8")
    user3 = User(name="linfun", uid="24238341", key="E3F3255F24B9B071C7F98E880BDC0382",
        idfa="D7641C67-53D9-4302-B0E6-338795AFB917", 
        openid="oFfv-s3m_ecL40zdVYzOND5_lG-I")
    user4 = User(name="ny", uid="24806519", key="9B111476D11387EE32C076022189FD41",
        idfa="99F4D3A2-3D96-4F53-B1E2-3179778308DD", 
        openid="oFfv-s7lJfM2r1H1UtKNBwNm3RGw")
    user5 = User(name="apache", uid="24100028", key="20CACDC7AC201F2DB7D1201984F3BBAA",
        idfa="A3AF8EC0-974C-415E-8F62-03196B59A923", 
        openid="oFfv-s2cYU9GaX1Kz98ki5RoRsAk")
    user6 = User(name="czd", uid="24839995", key="23A5793304CE1B63A222254C98738FF8",
        idfa="AC07D175-D624-4872-9071-4DA7B3695594",
        openid="oFfv-s8f5RhGss5m1Z2FsDgNCXIg")
    user7 = User(name="lft", uid="24260077", key="7DCF1968B8BE79447536C4A015AFD8E5",
        idfa="D221E8CF-BBA2-449D-8A19-876C27146421",
        openid="oFfv-sxR2n63-mXBVtFDa9MRBDiI")
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.add(user5)
    session.add(user6)
    session.add(user7)
    session.commit()

def delaytasks():
    try:
        os.remove("celerydb.data")
    except OSError:
        pass

    session = Session()
    users = session.query(User).all()

    for user in users:
        start(user)

def start(user):
    client = ShikeClient(user.uid, user.key, user.idfa)
    client.init()

    run.delay(client, user)

def celery():
    os.system("celery -A tasks worker --loglevel=debug")


if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "init":
        init()
    elif arg == "run":
        delaytasks()
    elif arg == "celery":
        celery()
    elif arg == "runcelery":
        delaytasks()
        celery()
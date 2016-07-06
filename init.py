# -*- coding: utf-8 -*-

from model import engine, Model, Session, User

Model.metadata.drop_all(engine)
Model.metadata.create_all(engine)

session = Session()

user = User(name="xvl", uid="24238341", key="E3F3255F24B9B071C7F98E880BDC0382",
    idfa="D7641C67-53D9-4302-B0E6-338795AFB917", 
    openid="oFfv-s3m_ecL40zdVYzOND5_lG-I")
    
session.add(user)
session.commit()
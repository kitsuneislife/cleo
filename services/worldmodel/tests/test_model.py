from services.worldmodel.model import make_default_model


def test_toymodel_predicts_deterministically():
    m = make_default_model()
    a = m.predict(b'hello')
    b = m.predict(b'hello')
    c = m.predict(b'world')
    assert a == b
    assert a != c

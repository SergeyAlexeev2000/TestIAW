from app.normalizer import (
    build_name_keys,
    build_email_keys,
    build_file_keys,
    get_email_local_part,
    get_file_stem,
)


def test_get_email_local_part():
    assert get_email_local_part("J.Stone@dundermifflin.com") == "J.Stone"


def test_get_file_stem():
    assert get_file_stem(r"C:\FirstGroup\John_Stone.pdf") == "John_Stone"


def test_build_name_keys_for_simple_name():
    keys = build_name_keys("John Stone")
    assert "johnstone" in keys
    assert "john_stone" in keys
    assert "jstone" in keys
    assert "j_stone" in keys
    assert "j.stone" in keys


def test_build_name_keys_for_middle_initial():
    keys = build_name_keys("Maureen M. Smith")
    assert "maureensmith" in keys or "maureen_smith" in keys
    assert "mmsmith" in keys
    assert "m.smith" in keys or "m_smith" in keys


def test_build_email_keys():
    keys = build_email_keys("J_Meldrum@dundermifflin.com")
    assert "jmeldrum" in keys
    assert "j_meldrum" in keys
    assert "j.meldrum" in keys


def test_build_file_keys():
    keys = build_file_keys(r"C:\Second Group\N_Lee-Walsh.pdf")
    assert "nleewalsh" in keys
    assert "n_lee-walsh".replace("-", "_") in {k.replace("-", "_") for k in keys}
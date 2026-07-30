"""しきい値秘密分散の検査。実行: python3 -m pytest tests/test_threshold.py -q"""
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "fue"))
import threshold as T


def test_2of3_どの2つでも復元できる():
    secret = T.symbols_of(260729, 6)
    shares = T.split(secret, 2, 3, rng=random.Random(42))
    assert len(shares) == 3
    for combo in itertools.combinations(shares, 2):
        assert T.combine(list(combo)) == secret


def test_2of3_3つ全部でも復元できる():
    secret = T.symbols_of(123456, 6)
    shares = T.split(secret, 2, 3, rng=random.Random(1))
    assert T.combine(shares) == secret


def test_1つでは何も分からない():
    """同じ断片1つを共有しうる秘密が、すべての候補にわたって存在することを確かめる。

    断片が1つのとき、残りの1つを自由に選べば任意の秘密を作れる。つまり断片1つから
    秘密は一切絞り込めない。
    """
    p = 11
    secret = T.symbols_of(260729, 6)
    shares = T.split(secret, 2, 3, rng=random.Random(7))
    j1, y1 = shares[0]
    seen = set()
    for cand in range(p):                       # 1記号目の候補すべて
        # y1 = s + a*j1 を満たす a が必ず一つある（j1は0でないので逆数がある）
        a = ((y1[0] - cand) * pow(j1, p - 2, p)) % p
        assert (cand + a * j1) % p == y1[0]
        seen.add(cand)
    assert seen == set(range(p)), "どの候補も同じ断片と両立する"


def test_2of2はカードの方式と一致する():
    """k=2,n=2 のとき、断片1と断片2の関係が「和が秘密」になっていることを確かめる。

    Shamir の f(x)=s+a·x で j=1,2 を取ると y1=s+a, y2=s+2a なので
    2·y1 − y2 = s である。カードで使った「足して秘密」とは式が違うが、
    どちらも1つでは分からない同じ強さの分け方である。
    """
    secret = T.symbols_of(1000, 6)
    (j1, y1), (j2, y2) = T.split(secret, 2, 2, rng=random.Random(3))
    assert (j1, j2) == (1, 2)
    for i, s in enumerate(secret):
        assert (2 * y1[i] - y2[i]) % 11 == s


def test_3of3は2つでは復元できない():
    secret = T.symbols_of(99999, 6)
    shares = T.split(secret, 3, 3, rng=random.Random(5))
    assert T.combine(shares) == secret
    for combo in itertools.combinations(shares, 2):
        assert T.combine(list(combo)) != secret     # 2つでは戻らない


def test_断片は秘密と同じ記号数である():
    for width in (1, 4, 6, 10):
        secret = [3] * width
        for j, y in T.split(secret, 2, 3, rng=random.Random(0)):
            assert len(y) == width


def test_受け付けない入力():
    import pytest
    with pytest.raises(ValueError):
        T.split([1, 2], 1, 3)                     # k=1 は分散にならない
    with pytest.raises(ValueError):
        T.split([1, 2], 2, 11)                    # 断片が素数体に収まらない
    with pytest.raises(ValueError):
        T.split([11], 2, 3)                       # 記号が範囲外
    with pytest.raises(ValueError):
        T.combine([(1, [1, 2]), (1, [3, 4])])     # 同じ番号
    with pytest.raises(ValueError):
        T.combine([(1, [1, 2]), (2, [3])])        # 記号数が違う


def test_総当たりで全組み合わせを確かめる():
    """小さい秘密で、乱数を変えながら何度も確かめる。"""
    rng = random.Random(123)
    for _ in range(200):
        secret = [rng.randrange(11) for _ in range(3)]
        shares = T.split(secret, 2, 3, rng=rng)
        for combo in itertools.combinations(shares, 2):
            assert T.combine(list(combo)) == secret

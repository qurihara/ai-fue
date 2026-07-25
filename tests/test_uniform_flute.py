"""外形長を揃えた内部壁式の半割り笛テスト。pytest なしでも実行できる。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import trimesh

from fue import cipherflute, halfcut


def _slice_volume(mesh, x_center, reference):
    """x_center を中心とする厚さ1mmの帯を切り出し、その中の体積を返す。"""
    slab = trimesh.creation.box(
        extents=[1.0, reference.extents[1] + 2.0, reference.extents[2] + 2.0],
        transform=trimesh.transformations.translation_matrix(
            [x_center, *reference.bounds.mean(axis=0)[1:]]))
    return trimesh.boolean.intersection([mesh, slab], engine="manifold").volume


def test_uniform_body_flute():
    L, L_max = 50.0, 74.7
    uniform = halfcut.uniform_body_flute(L, L_max=L_max)
    longest = halfcut.half_flute(L_max)
    assert uniform.is_watertight
    assert np.allclose(uniform.extents, longest.extents, atol=0.1)

    # ボアを塞ぐ壁があることを、位置を決め打ちせずに走査して確かめる。
    # 壁は音の管長 L より頭側に置かれ、さらに _wall_flat_correction のぶんだけ
    # 寄る（空洞のたわみで下がる音を先取りして補償するため）。補償の値を変えると
    # 壁の位置も動くので、特定の x に固定した検査はすぐ古くなる。ここでは
    # 「L の手前のどこかに、体積がはっきり増える帯がある」ことだけを見る。
    xs = np.arange(L - 10.0, L + 1.0, 1.0)
    ratios = [_slice_volume(uniform, x, longest) / _slice_volume(longest, x, longest)
              for x in xs]
    best = int(np.argmax(ratios))
    assert ratios[best] > 1.05, "ボアを塞ぐ壁が見つからない"
    assert xs[best] < L, "壁は音の管長より頭側にあるはず"


def test_equal_length_has_no_wall():
    length = 50.0
    uniform = halfcut.uniform_body_flute(length, L_max=length)
    plain = halfcut.half_flute(length)
    assert np.isclose(uniform.volume, plain.volume, rtol=1e-6, atol=1e-6)


def test_uniform_comb():
    comb, infos, notes, lengths = cipherflute.build_uniform_comb(["F6", "A6", "D#7"])
    assert comb.is_watertight
    assert notes == ["D#7", "A6", "F6"]
    assert len({round(info["x_foot"], 1) for info in infos}) == 1
    # 外形は最長音そのものではなく、最長音より長く揃える。そうすると最長の笛にも
    # 壁が入り、「最長だけ壁なし」という例外がなくなって全笛の挙動がそろう
    # （較正のずれが残っても基準笛と同じように出て相殺される）。
    # 余白の値そのものは設計上の選択なので、ここでは定数に依らず
    # 「最長の管長より外形が長い」という目的そのものを確かめる。
    assert infos[0]["x_foot"] > round(max(lengths), 1), "最長の笛にも壁が入る余白が要る"
    assert infos[0]["x_foot"] == round(max(lengths) + cipherflute.WALL_MARGIN, 1)


if __name__ == "__main__":
    test_uniform_body_flute()
    test_equal_length_has_no_wall()
    test_uniform_comb()
    print("uniform flute tests: OK")

"""外形長を揃えた内部壁式の半割り笛テスト。pytest なしでも実行できる。"""
import numpy as np
import trimesh

from fue import cipherflute, halfcut


def test_uniform_body_flute():
    uniform = halfcut.uniform_body_flute(50, L_max=74.7)
    longest = halfcut.half_flute(74.7)
    assert uniform.is_watertight
    assert np.allclose(uniform.extents, longest.extents, atol=0.1)

    # x=46mm から薄いスライス内の体積増加で、ボアを塞ぐ壁を確認する。
    slab = trimesh.creation.box(
        extents=[1.0, longest.extents[1] + 2.0, longest.extents[2] + 2.0],
        transform=trimesh.transformations.translation_matrix(
            [46.5, *longest.bounds.mean(axis=0)[1:]]))
    plain_slice = trimesh.boolean.intersection([longest, slab], engine="manifold")
    wall_slice = trimesh.boolean.intersection([uniform, slab], engine="manifold")
    assert wall_slice.volume > plain_slice.volume * 1.05


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
    assert infos[0]["x_foot"] == round(max(lengths), 1)


if __name__ == "__main__":
    test_uniform_body_flute()
    test_equal_length_has_no_wall()
    test_uniform_comb()
    print("uniform flute tests: OK")

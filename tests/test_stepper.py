from core.stepper import Stepper


def test_stepper_navigation() -> None:
    steps = ["a", "b", "c"]
    sp = Stepper(steps=steps, index=0)

    assert sp.current() == "a"
    assert sp.can_prev() is False
    assert sp.can_next() is True

    sp.next()
    assert sp.current() == "b"
    assert sp.can_prev() is True
    assert sp.can_next() is True

    sp.next()
    assert sp.current() == "c"
    assert sp.can_next() is False

    sp.prev()
    assert sp.current() == "b"

    sp.reset()
    assert sp.current() == "a"

def test_singleton():
    from trame.app.singleton import Singleton

    @Singleton
    def new_object():
        return object()

    # Normally, a new object would be returned each time
    # However, since this is a singleton, the same object should be returned
    assert new_object() is new_object()

import pytest

from demo.streamlit_test.streamlit_test import streamlit_test


def test_streamlit_test():
    with pytest.raises(TypeError):
        streamlit_test()



from src.core.text_manager import TextManager


def test_text_manager_word_count_scaling():
    tm = TextManager()
    for level in ["beginner", "intermediate", "advanced", "expert"]:
        text_30 = tm.get_text(level, 30)
        text_60 = tm.get_text(level, 60)
        assert len(text_60.split()) >= len(text_30.split())
        assert len(text_30.split()) == int(30 * 2.5)
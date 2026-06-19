"""Тесты критериев приёмки ML-субтитров (subtitle_qa.captions_ok).

Позитивный кейс плюс по одному негативному на каждый критерий и граничный
анализ порога длины слова.
"""
import pytest
from subtitle_qa import captions_ok


def test_good_captions_pass():
    events = [(0.0, 0.6), (0.7, 1.2), (1.3, 2.0), (2.1, 2.8), (3.0, 3.6)]
    ok, reasons = captions_ok(events, audio_duration=4.0)
    assert ok is True
    assert reasons == []


def test_empty_fails():
    ok, reasons = captions_ok([], audio_duration=4.0)
    assert ok is False
    assert any("нет событ" in r for r in reasons)


def test_non_monotonic_fails():
    events = [(0.0, 0.6), (2.0, 2.5), (1.0, 1.4)]
    ok, reasons = captions_ok(events, audio_duration=4.0)
    assert ok is False
    assert any("монотон" in r for r in reasons)


def test_word_too_long_fails():
    events = [(0.0, 0.6), (0.7, 5.0)]
    ok, reasons = captions_ok(events, audio_duration=6.0)
    assert ok is False
    assert any("длиннее" in r for r in reasons)


def test_low_coverage_fails():
    events = [(0.0, 0.3), (0.3, 0.6)]
    ok, reasons = captions_ok(events, audio_duration=30.0)
    assert ok is False
    assert any("покрытие" in r for r in reasons)


@pytest.mark.parametrize("word_len,should_pass", [
    (3.0, True),
    (3.5, True),
    (3.6, False),
])
def test_word_duration_boundary(word_len, should_pass):
    events = [(0.0, 0.5), (1.0, 1.0 + word_len)]
    ok, _ = captions_ok(events, audio_duration=word_len + 5)
    assert ok is should_pass

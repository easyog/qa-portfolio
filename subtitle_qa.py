"""Критерии приёмки для вывода ML-субтитров (forced alignment).

Вывод модели недетерминирован, эталонного результата нет, поэтому качество
проверяется по метрикам, а не сравнением с фиксированным ожиданием:
  1. монотонность   — старты событий идут по возрастанию;
  2. длина слова    — событие не висит на экране дольше порога;
  3. покрытие       — события покрывают разумную долю длительности аудио.

Возвращает (ok: bool, reasons: list[str]).
"""
from __future__ import annotations

MAX_WORD_SEC = 3.5
MIN_COVERAGE = 0.30


def captions_ok(events, audio_duration, max_word_sec=MAX_WORD_SEC,
                min_coverage=MIN_COVERAGE):
    """events: список (start, end) в секундах; audio_duration: длительность аудио."""
    reasons = []

    if not events:
        return False, ["нет событий субтитров"]

    starts = [s for s, _ in events]
    if any(b < a for a, b in zip(starts, starts[1:])):
        reasons.append("старты не монотонны")

    too_long = [(s, e) for s, e in events if (e - s) > max_word_sec]
    if too_long:
        reasons.append(f"{len(too_long)} событий длиннее {max_word_sec}с")

    span = max(e for _, e in events) - min(s for s, _ in events)
    coverage = span / audio_duration if audio_duration else 0
    if coverage < min_coverage:
        reasons.append(f"покрытие {coverage:.0%} < {min_coverage:.0%}")

    return (len(reasons) == 0), reasons

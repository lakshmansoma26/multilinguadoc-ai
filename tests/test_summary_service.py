from services.summary_service import generate_summary


def test_generate_summary_function_exists():
    assert callable(generate_summary)
from services.study_service import generate_study_material


def test_generate_study_material_function_exists():
    assert callable(generate_study_material)
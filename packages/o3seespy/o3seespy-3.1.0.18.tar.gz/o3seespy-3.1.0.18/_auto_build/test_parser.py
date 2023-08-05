from _auto_build import run


def test_check_default_is_an_expression():
    assert run.check_if_default_is_expression('a2*w')
    assert run.check_if_default_is_expression('a2/w')
    assert run.check_if_default_is_expression('a2+w')
    assert run.check_if_default_is_expression('a2-w')
    assert run.check_if_default_is_expression('a2^w')


def test_convert_to_camel():
    print(run.convert_camel_to_snake('Contact2D'))

def test_convert_to_snake():
    print(run.convert_camel_to_snake('Contact2D'))


if __name__ == '__main__':
    test_convert_to_snake()

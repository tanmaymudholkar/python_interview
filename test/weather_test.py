from interview import weather
import io

# def test_replace_me():
#     reader = io.StringIO("Line One\nLine Two\n")
#     writer = io.StringIO()
#     weather.process_csv(reader, writer)
#     assert writer.getvalue() == "Saw 2 lines\n"

def test_process_csv():
    with open('data/chicago_beach_weather_test.csv') as reader:
        writer = io.StringIO()
        weather.process_csv(reader, writer)
        with open('data/chicago_beach_weather_test_expected_output.csv') as test_template:
            expected = ''.join(test_template.readlines())
        assert writer.getvalue() == expected

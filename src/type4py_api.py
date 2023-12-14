import json
from typing import Any, Dict, List
import requests
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Type4PyException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class TypeT5Exception(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def get_ordered_type4py_predictions(python_code: str) -> List[Dict[str, Any]]:
    # r = requests.post("https://type4py.com/api/predict?tc=0", f.read())
    response = requests.post("http://localhost:5001/api/predict?tc=0", python_code)
    json_response = response.json()

    if json_response["error"] is not None:
        raise Type4PyException(json_response["error"])

    functions_predictions = {}
    for class_obj in json_response["response"]["classes"]:
        for func in class_obj["funcs"]:
            location_index = func["fn_lc"][0][0]
            functions_predictions[location_index] = func

    for func in json_response["response"]["funcs"]:
        location_index = func["fn_lc"][0][0]
        functions_predictions[location_index] = func

    functions_predictions = dict(sorted(functions_predictions.items()))
    functions_predictions = functions_predictions.values()

    filter_fields = ["q_name", "params_p", "ret_type_p"]
    type_predictions = list(
        map(
            lambda f: {key: f[key] for key in f if key in filter_fields},
            functions_predictions,
        )
    )
    return type_predictions


# Get ML predictions from Type4Py API without ordering by location
def get_typet5_predictions() -> List[Dict[str, Any]]:
    # r = requests.post("https://type4py.com/api/predict?tc=0", f.read())
    # response = requests.post("http://localhost:5000/api", f.read())
    response = """
    {"error": null, "responses": [{"file_path": "ansi.py", "response": {"classes": [{"name": "AnsiCodes", "q_name": "AnsiCodes", "funcs": [{"name": "__init__", "q_name": "AnsiCodes.__init__", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}, {"name": "AnsiCursor", "q_name": "AnsiCursor", "funcs": [{"name": "UP", "q_name": "AnsiCursor.UP", "params_p": {"n": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "DOWN", "q_name": "AnsiCursor.DOWN", "params_p": {"n": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "FORWARD", "q_name": "AnsiCursor.FORWARD", "params_p": {"n": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "BACK", "q_name": "AnsiCursor.BACK", "params_p": {"n": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "POS", "q_name": "AnsiCursor.POS", "params_p": {"x": [["int", 1.0]], "y": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}]}], "funcs": [{"name": "code_to_chars", "q_name": "code_to_chars", "params_p": {"code": [["str", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "set_title", "q_name": "set_title", "params_p": {"title": [["str", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "clear_screen", "q_name": "clear_screen", "params_p": {"mode": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "clear_line", "q_name": "clear_line", "params_p": {"mode": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}]}}, {"file_path": "ansitowin32.py", "response": {"classes": [{"name": "StreamWrapper", "q_name": "StreamWrapper", "funcs": [{"name": "__init__", "q_name": "StreamWrapper.__init__", "params_p": {"wrapped": [["Callable", 1.0]], "converter": [["Callable", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "__getattr__", "q_name": "StreamWrapper.__getattr__", "params_p": {"name": [["str", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "__enter__", "q_name": "StreamWrapper.__enter__", "params_p": {"args": [["Any", 1.0]], "kwargs": [["Any", 1.0]]}, "ret_type_p": [["Any", 1.0]]}, {"name": "__exit__", "q_name": "StreamWrapper.__exit__", "params_p": {"args": [["Any", 1.0]], "kwargs": [["Any", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "__setstate__", "q_name": "StreamWrapper.__setstate__", "params_p": {"state": [["dict", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "__getstate__", "q_name": "StreamWrapper.__getstate__", "params_p": {}, "ret_type_p": [["dict", 1.0]]}, {"name": "closed", "q_name": "StreamWrapper.closed", "params_p": {}, "ret_type_p": [["bool", 1.0]]}, {"name": "isatty", "q_name": "StreamWrapper.isatty", "params_p": {}, "ret_type_p": [["bool", 1.0]]}, {"name": "write", "q_name": "StreamWrapper.write", "params_p": {"text": [["str", 1.0]]}, "ret_type_p": [["None", 1.0]]}]}, {"name": "AnsiToWin32", "q_name": "AnsiToWin32", "funcs": [{"name": "should_wrap", "q_name": "AnsiToWin32.should_wrap", "params_p": {}, "ret_type_p": [["bool", 1.0]]}, {"name": "extract_params", "q_name": "AnsiToWin32.extract_params", "params_p": {"command": [["str", 1.0]], "paramstring": [["str", 1.0]]}, "ret_type_p": [["tuple", 1.0]]}, {"name": "flush", "q_name": "AnsiToWin32.flush", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "call_win32", "q_name": "AnsiToWin32.call_win32", "params_p": {"command": [["str", 1.0]], "params": [["tuple", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "convert_ansi", "q_name": "AnsiToWin32.convert_ansi", "params_p": {"paramstring": [["str", 1.0]], "command": [["str", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "convert_osc", "q_name": "AnsiToWin32.convert_osc", "params_p": {"text": [["str", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "write_and_convert", "q_name": "AnsiToWin32.write_and_convert", "params_p": {"text": [["str", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "write", "q_name": "AnsiToWin32.write", "params_p": {"text": [["str", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "write_plain_text", "q_name": "AnsiToWin32.write_plain_text", "params_p": {"text": [["str", 1.0]], "start": [["int", 1.0]], "end": [["int", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "reset_all", "q_name": "AnsiToWin32.reset_all", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "get_win32_calls", "q_name": "AnsiToWin32.get_win32_calls", "params_p": {}, "ret_type_p": [["dict", 1.0]]}, {"name": "__init__", "q_name": "AnsiToWin32.__init__", "params_p": {"wrapped": [["Callable", 1.0]], "convert": [["bool", 1.0]], "strip": [["bool", 1.0]], "autoreset": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}]}], "funcs": []}}, {"file_path": "initialise.py", "response": {"classes": [], "funcs": [{"name": "deinit", "q_name": "deinit", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "reinit", "q_name": "reinit", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "wrap_stream", "q_name": "wrap_stream", "params_p": {"stream": [["Callable", 1.0]], "convert": [["bool", 1.0]], "strip": [["bool", 1.0]], "autoreset": [["bool", 1.0]], "wrap": [["bool", 1.0]]}, "ret_type_p": [["Callable", 1.0]]}, {"name": "just_fix_windows_console", "q_name": "just_fix_windows_console", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "reset_all", "q_name": "reset_all", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "init", "q_name": "init", "params_p": {"autoreset": [["bool", 1.0]], "convert": [["bool", 1.0]], "strip": [["bool", 1.0]], "wrap": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "colorama_text", "q_name": "colorama_text", "params_p": {"args": [["str", 1.0]], "kwargs": [["str", 1.0]]}, "ret_type_p": [["AbstractContextManager", 1.0]]}, {"name": "_wipe_internal_state_for_tests", "q_name": "_wipe_internal_state_for_tests", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}}, {"file_path": "tests/ansitowin32_test.py", "response": {"classes": [{"name": "StreamWrapperTest", "q_name": "StreamWrapperTest", "funcs": [{"name": "testIsAProxy", "q_name": "StreamWrapperTest.testIsAProxy", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_closed_shouldnt_raise_on_closed_stream", "q_name": "StreamWrapperTest.test_closed_shouldnt_raise_on_closed_stream", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_closed_shouldnt_raise_on_detached_stream", "q_name": "StreamWrapperTest.test_closed_shouldnt_raise_on_detached_stream", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testProxyNoContextManager", "q_name": "StreamWrapperTest.testProxyNoContextManager", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testDelegatesContext", "q_name": "StreamWrapperTest.testDelegatesContext", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testDelegatesWrite", "q_name": "StreamWrapperTest.testDelegatesWrite", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}, {"name": "AnsiToWin32Test", "q_name": "AnsiToWin32Test", "funcs": [{"name": "test_native_windows_ansi", "q_name": "AnsiToWin32Test.test_native_windows_ansi", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_osc_codes", "q_name": "AnsiToWin32Test.test_osc_codes", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testCallWin32UsesLookup", "q_name": "AnsiToWin32Test.testCallWin32UsesLookup", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testExtractParams", "q_name": "AnsiToWin32Test.testExtractParams", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_wrap_shouldnt_raise_on_missing_closed_attr", "q_name": "AnsiToWin32Test.test_wrap_shouldnt_raise_on_missing_closed_attr", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_wrap_shouldnt_raise_on_closed_orig_stdout", "q_name": "AnsiToWin32Test.test_wrap_shouldnt_raise_on_closed_orig_stdout", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_reset_all_shouldnt_raise_on_closed_orig_stdout", "q_name": "AnsiToWin32Test.test_reset_all_shouldnt_raise_on_closed_orig_stdout", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteAndConvertCallsWin32WithParamsAndCommand", "q_name": "AnsiToWin32Test.testWriteAndConvertCallsWin32WithParamsAndCommand", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteAndConvertSkipsEmptySnippets", "q_name": "AnsiToWin32Test.testWriteAndConvertSkipsEmptySnippets", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteAndConvertStripsAllValidAnsi", "q_name": "AnsiToWin32Test.testWriteAndConvertStripsAllValidAnsi", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteAndConvertWritesPlainText", "q_name": "AnsiToWin32Test.testWriteAndConvertWritesPlainText", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "assert_autoresets", "q_name": "AnsiToWin32Test.assert_autoresets", "params_p": {"convert": [["bool", 1.0]], "autoreset": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteAutoresets", "q_name": "AnsiToWin32Test.testWriteAutoresets", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteDoesNotStripAnsi", "q_name": "AnsiToWin32Test.testWriteDoesNotStripAnsi", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testWriteStripsAnsi", "q_name": "AnsiToWin32Test.testWriteStripsAnsi", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testStripIsFalseOffWindows", "q_name": "AnsiToWin32Test.testStripIsFalseOffWindows", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testStripIsTrueOnWindows", "q_name": "AnsiToWin32Test.testStripIsTrueOnWindows", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInit", "q_name": "AnsiToWin32Test.testInit", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}], "funcs": []}}, {"file_path": "tests/ansi_test.py", "response": {"classes": [{"name": "AnsiTest", "q_name": "AnsiTest", "funcs": [{"name": "setUp", "q_name": "AnsiTest.setUp", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "tearDown", "q_name": "AnsiTest.tearDown", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testForeAttributes", "q_name": "AnsiTest.testForeAttributes", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testBackAttributes", "q_name": "AnsiTest.testBackAttributes", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testStyleAttributes", "q_name": "AnsiTest.testStyleAttributes", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}], "funcs": []}}, {"file_path": "tests/initialise_test.py", "response": {"classes": [{"name": "InitTest", "q_name": "InitTest", "funcs": [{"name": "assertWrapped", "q_name": "InitTest.assertWrapped", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "assertNotWrapped", "q_name": "InitTest.assertNotWrapped", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "setUp", "q_name": "InitTest.setUp", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testAtexitRegisteredOnlyOnce", "q_name": "InitTest.testAtexitRegisteredOnlyOnce", "params_p": {"mockRegister": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testAutoResetChangeable", "q_name": "InitTest.testAutoResetChangeable", "params_p": {"mockATW32": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testAutoResetPassedOn", "q_name": "InitTest.testAutoResetPassedOn", "params_p": {"mockATW32": [["Mock", 1.0]], "_": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitWrapOffIncompatibleWithAutoresetOn", "q_name": "InitTest.testInitWrapOffIncompatibleWithAutoresetOn", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitWrapOffDoesntWrapOnWindows", "q_name": "InitTest.testInitWrapOffDoesntWrapOnWindows", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitAutoresetOnWrapsOnAllPlatforms", "q_name": "InitTest.testInitAutoresetOnWrapsOnAllPlatforms", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitDoesntWrapIfNone", "q_name": "InitTest.testInitDoesntWrapIfNone", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitDoesntWrapOnNonWindows", "q_name": "InitTest.testInitDoesntWrapOnNonWindows", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitDoesntWrapOnEmulatedWindows", "q_name": "InitTest.testInitDoesntWrapOnEmulatedWindows", "params_p": {"_": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testInitWrapsOnWindows", "q_name": "InitTest.testInitWrapsOnWindows", "params_p": {"_": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "tearDown", "q_name": "InitTest.tearDown", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}, {"name": "JustFixWindowsConsoleTest", "q_name": "JustFixWindowsConsoleTest", "funcs": [{"name": "_reset", "q_name": "JustFixWindowsConsoleTest._reset", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testJustFixWindowsConsole", "q_name": "JustFixWindowsConsoleTest.testJustFixWindowsConsole", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "tearDown", "q_name": "JustFixWindowsConsoleTest.tearDown", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}], "funcs": []}}, {"file_path": "tests/utils.py", "response": {"classes": [{"name": "StreamTTY", "q_name": "StreamTTY", "funcs": [{"name": "isatty", "q_name": "StreamTTY.isatty", "params_p": {}, "ret_type_p": [["bool", 1.0]]}]}, {"name": "StreamNonTTY", "q_name": "StreamNonTTY", "funcs": [{"name": "isatty", "q_name": "StreamNonTTY.isatty", "params_p": {}, "ret_type_p": [["bool", 1.0]]}]}], "funcs": [{"name": "osname", "q_name": "osname", "params_p": {"name": [["str", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "replace_by", "q_name": "replace_by", "params_p": {"stream": [["Stream", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "replace_original_by", "q_name": "replace_original_by", "params_p": {"stream": [["Stream", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "pycharm", "q_name": "pycharm", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}}, {"file_path": "tests/isatty_test.py", "response": {"classes": [{"name": "IsattyTest", "q_name": "IsattyTest", "funcs": [{"name": "test_withPycharmNoneOverride", "q_name": "IsattyTest.test_withPycharmNoneOverride", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_withPycharmNonTTYOverride", "q_name": "IsattyTest.test_withPycharmNonTTYOverride", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_withPycharmTTYOverride", "q_name": "IsattyTest.test_withPycharmTTYOverride", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_withPycharm", "q_name": "IsattyTest.test_withPycharm", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_nonTTY", "q_name": "IsattyTest.test_nonTTY", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_TTY", "q_name": "IsattyTest.test_TTY", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "test_withPycharmStreamWrapped", "q_name": "IsattyTest.test_withPycharmStreamWrapped", "params_p": {}, "ret_type_p": [["None", 1.0]]}]}], "funcs": [{"name": "is_a_tty", "q_name": "is_a_tty", "params_p": {"stream": [["Stream", 1.0]]}, "ret_type_p": [["bool", 1.0]]}]}}, {"file_path": "win32.py", "response": {"classes": [{"name": "CONSOLE_SCREEN_BUFFER_INFO", "q_name": "CONSOLE_SCREEN_BUFFER_INFO", "funcs": [{"name": "__str__", "q_name": "CONSOLE_SCREEN_BUFFER_INFO.__str__", "params_p": {}, "ret_type_p": [["str", 1.0]]}]}], "funcs": [{"name": "_winapi_test", "q_name": "_winapi_test", "params_p": {"handle": [["int", 1.0]]}, "ret_type_p": [["bool", 1.0]]}, {"name": "winapi_test", "q_name": "winapi_test", "params_p": {}, "ret_type_p": [["bool", 1.0]]}, {"name": "GetConsoleScreenBufferInfo", "q_name": "GetConsoleScreenBufferInfo", "params_p": {"stream_id": [["int", 1.0]]}, "ret_type_p": [["CONSOLE_SCREEN_BUFFER_INFO", 1.0]]}, {"name": "SetConsoleTextAttribute", "q_name": "SetConsoleTextAttribute", "params_p": {"stream_id": [["int", 1.0]], "attrs": [["win32.Attributes", 1.0]]}, "ret_type_p": [["Callable", 1.0]]}, {"name": "SetConsoleCursorPosition", "q_name": "SetConsoleCursorPosition", "params_p": {"stream_id": [["int", 1.0]], "position": [["tuple", 1.0]], "adjust": [["bool", 1.0]]}, "ret_type_p": [["Callable", 1.0]]}, {"name": "FillConsoleOutputCharacter", "q_name": "FillConsoleOutputCharacter", "params_p": {"stream_id": [["int", 1.0]], "char": [["str", 1.0]], "length": [["int", 1.0]], "start": [["int", 1.0]]}, "ret_type_p": [["int", 1.0]]}, {"name": "FillConsoleOutputAttribute", "q_name": "FillConsoleOutputAttribute", "params_p": {"stream_id": [["int", 1.0]], "attr": [["int", 1.0]], "length": [["int", 1.0]], "start": [["int", 1.0]]}, "ret_type_p": [["int", 1.0]]}, {"name": "SetConsoleTitle", "q_name": "SetConsoleTitle", "params_p": {"title": [["str", 1.0]]}, "ret_type_p": [["Callable[[str], str]", 1.0]]}, {"name": "GetConsoleMode", "q_name": "GetConsoleMode", "params_p": {"handle": [["str", 1.0]]}, "ret_type_p": [["int", 1.0]]}, {"name": "SetConsoleMode", "q_name": "SetConsoleMode", "params_p": {"handle": [["str", 1.0]], "mode": [["int", 1.0]]}, "ret_type_p": [["None", 1.0]]}]}}, {"file_path": "winterm.py", "response": {"classes": [{"name": "WinTerm", "q_name": "WinTerm", "funcs": [{"name": "set_attrs", "q_name": "WinTerm.set_attrs", "params_p": {"value": [["win32.Attributes", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "get_attrs", "q_name": "WinTerm.get_attrs", "params_p": {}, "ret_type_p": [["win32.Attributes", 1.0]]}, {"name": "__init__", "q_name": "WinTerm.__init__", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "set_console", "q_name": "WinTerm.set_console", "params_p": {"attrs": [["win32.Attributes", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "style", "q_name": "WinTerm.style", "params_p": {"style": [["win32.Attributes", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "back", "q_name": "WinTerm.back", "params_p": {"back": [["win32.Attributes", 1.0]], "light": [["bool", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "fore", "q_name": "WinTerm.fore", "params_p": {"fore": [["win32.Attributes", 1.0]], "light": [["bool", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "reset_all", "q_name": "WinTerm.reset_all", "params_p": {"on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "get_position", "q_name": "WinTerm.get_position", "params_p": {"handle": [["int", 1.0]]}, "ret_type_p": [["tuple", 1.0]]}, {"name": "set_cursor_position", "q_name": "WinTerm.set_cursor_position", "params_p": {"position": [["tuple", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "cursor_adjust", "q_name": "WinTerm.cursor_adjust", "params_p": {"x": [["int", 1.0]], "y": [["int", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "erase_screen", "q_name": "WinTerm.erase_screen", "params_p": {"mode": [["int", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "erase_line", "q_name": "WinTerm.erase_line", "params_p": {"mode": [["int", 1.0]], "on_stderr": [["bool", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "set_title", "q_name": "WinTerm.set_title", "params_p": {"title": [["str", 1.0]]}, "ret_type_p": [["None", 1.0]]}]}], "funcs": [{"name": "get_osfhandle", "q_name": "get_osfhandle", "params_p": {"_": [["int", 1.0]]}, "ret_type_p": [["str", 1.0]]}, {"name": "enable_vt_processing", "q_name": "enable_vt_processing", "params_p": {"fd": [["int", 1.0]]}, "ret_type_p": [["bool", 1.0]]}]}}, {"file_path": "tests/winterm_test.py", "response": {"classes": [{"name": "WinTermTest", "q_name": "WinTermTest", "funcs": [{"name": "testGetAttrs", "q_name": "WinTermTest.testGetAttrs", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testInit", "q_name": "WinTermTest.testInit", "params_p": {"mockWin32": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testSetConsoleOnStderr", "q_name": "WinTermTest.testSetConsoleOnStderr", "params_p": {"mockWin32": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testSetConsole", "q_name": "WinTermTest.testSetConsole", "params_p": {"mockWin32": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}, {"name": "testStyle", "q_name": "WinTermTest.testStyle", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testBack", "q_name": "WinTermTest.testBack", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testFore", "q_name": "WinTermTest.testFore", "params_p": {}, "ret_type_p": [["None", 1.0]]}, {"name": "testResetAll", "q_name": "WinTermTest.testResetAll", "params_p": {"mockWin32": [["Mock", 1.0]]}, "ret_type_p": [["None", 1.0]]}]}], "funcs": []}}]}
    """
    # json_response = response.json()
    json_response = json.loads(response)

    if json_response["error"] is not None:
        raise TypeT5Exception(json_response["error"])

    type_predictions_per_file = {}
    for file_response in json_response["responses"]:
        functions_predictions = []
        for class_obj in file_response["response"]["classes"]:
            functions_predictions += class_obj["funcs"]

        functions_predictions += file_response["response"]["funcs"]

        filter_fields = ["q_name", "params_p", "ret_type_p"]
        type_predictions = list(
            map(
                lambda f: {key: f[key] for key in f if key in filter_fields},
                functions_predictions,
            )
        )
        type_predictions_per_file[file_response["file_path"]] = type_predictions
    return type_predictions_per_file

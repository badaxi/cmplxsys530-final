"""Unit tests for LogWriter."""

from os import listdir, remove
from os.path import isfile, join

from uuid import uuid4
from log_manager.log_writer import LogWriter
from log_manager.log_reader import LogReader
import config

# Prefix for files generated by this function
TEST_ID = str(uuid4())


def test_writer_basic():
    """Basic test for LogWriter class."""
    header = ["test1", "test2", "test3"]
    lw1 = LogWriter(header=header, prefix=TEST_ID)

    dict_to_write = {}
    dict_to_write["test1"] = "pew"
    dict_to_write["test2"] = "foo"
    dict_to_write["test3"] = "bar"

    lw1.write_line(dict_to_write)


def test_prefix_handling():
    """Test prefix validation for LogWriter."""
    # Invalid tab character
    catch_err_1 = False
    try:
        _ = LogWriter(header=["test"], prefix="\test")
    except AttributeError:
        catch_err_1 = True

    assert catch_err_1

    # Invalid backslash
    catch_err_2 = False
    try:
        _ = LogWriter(header=["test"], prefix="/test")
    except AttributeError:
        catch_err_2 = True
    assert catch_err_2

    # Invalid dot character
    catch_err_3 = False
    try:
        _ = LogWriter(header=["test"], prefix=".test")
    except AttributeError:
        catch_err_3 = True
    assert catch_err_3


def test_header_validation():
    """Test logic for checking header."""
    catch_err = False
    try:
        _ = LogWriter(header=[])
    except AttributeError:
        catch_err = True

    assert catch_err


def cleanup():
    """Clean up logs for this run."""
    log_files = [join(config.LOG_DIR, f) for f in listdir(config.LOG_DIR)
                 if isfile(join(config.LOG_DIR, f))]
    for file_ in log_files:
        if TEST_ID in file_:
            remove(file_)


test_writer_basic()
test_prefix_handling()
test_header_validation()

cleanup()

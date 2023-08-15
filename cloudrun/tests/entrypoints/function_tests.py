"""
Tess configuration for the Function child class
"""

# --------------------------------------------------------------------------------------
# cmd

BAD_COMMAND_FORMAT = {
    "type": "python",
    "src": "scripts",
    "cmd": "scripts.test_fn.hello_world"
}


# --------------------------------------------------------------------------------------
# kwargs

BAD_KWARGS = {
    "type": "python",
    "src": "scripts",
    "cmd": "test_fn.hello_world",
    "kwargs": [
        "VALUE1"
    ]
}

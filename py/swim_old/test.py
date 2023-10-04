obj = {
    "a": {
        "100m": {
            "back": {
                "Times": {
                    10,
                    20,
                    30
                }
            }
        }
    }
}

print(obj["a"])

obj["a"] = {
    "200m": {
        "back": {
            "Times": {
                10,
                20,
                30
            }
        }
    }
}

print(obj["a"])

obj["b"] = 10

print(obj["b"])
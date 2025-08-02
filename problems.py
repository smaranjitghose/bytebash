EXAMPLE_PROBLEMS = {
    "Beginner: Sum of Two Numbers": {
        "description": "Read two integers and calculate their sum - Entry level problem for new learners",
        "code": "# Read two integers and print their sum\na = int(input())\nb = int(input())\nprint(a + b)",
        "test_cases": [
            ("5\n3", "8"),
            ("10\n-2", "8"),
            ("0\n0", "0"),
            ("-5\n7", "2"),
            ("100\n200", "300"),
            ("15\n-15", "0"),
            ("999\n1", "1000")
        ]
    },
    "Intermediate: Even or Odd": {
        "description": "Determine if a given number is even or odd - Logic and conditionals practice",
        "code": "# Check if a number is even or odd\nn = int(input())\nif n % 2 == 0:\n    print(\"Even\")\nelse:\n    print(\"Odd\")",
        "test_cases": [
            ("4", "Even"),
            ("7", "Odd"),
            ("0", "Even"),
            ("1", "Odd"),
            ("100", "Even"),
            ("999", "Odd"),
            ("-2", "Even")
        ]
    },
    "Advanced: Maximum of Three": {
        "description": "Find the largest among three numbers - Multiple comparisons and edge case handling",
        "code": "# Find the maximum of three numbers\na = int(input())\nb = int(input())\nc = int(input())\nprint(max(a, b, c))",
        "test_cases": [
            ("5\n8\n3", "8"),
            ("10\n10\n10", "10"),
            ("1\n2\n3", "3"),
            ("100\n50\n75", "100"),
            ("-1\n-5\n-3", "-1"),
            ("0\n1\n-1", "1"),
            ("999\n1000\n998", "1000")
        ]
    }
}
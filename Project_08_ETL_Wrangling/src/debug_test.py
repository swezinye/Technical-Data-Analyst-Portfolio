# debug_test.py
import pandas as pd
from analyzeWords import analyzeWords

test_words = pd.Series([
    "apple", "book", "cool", "door", "elephant",
    "food", "good", "hello", "interesting", "zoo",
    "a", "be", "MOON", "balloon", "school"
])

result = analyzeWords(test_words)

print("YOUR oo_words:")
print(result['oo_words'].tolist())
print("\nYOUR words_6plus:")
print(result['words_6plus'].tolist())


import shelve
with shelve.open('expected_results') as exp:
    data = exp['analyzeWords']
    print("EXPECTED oo_words:")
    print(data['oo_words'].tolist())
    print("\nEXPECTED words_6plus:")
    print(data['words_6plus'].tolist())

    # diagnostic.py
    import pandas as pd
    import shelve
    from analyzeWords import analyzeWords

    # Load the professor's data
    with shelve.open('expected_results') as exp:
        data = exp['analyzeWords']
        test_input = data['input_data']  # Get the actual input data
        expected = exp['analyzeWords']

    # Run your function
    result = analyzeWords(test_input)

    # Compare oo_words
    print("OO_WORDS COMPARISON:")
    print(f"Expected length: {len(expected['oo_words'])}")
    print(f"Your length: {len(result['oo_words'])}")
    print(f"Lengths match: {len(expected['oo_words']) == len(result['oo_words'])}")

    if len(expected['oo_words']) == len(result['oo_words']):
        print("\nFirst 10 expected:", expected['oo_words'][:10].tolist())
        print("First 10 yours:", result['oo_words'][:10].tolist())

        # Check for differences
        diff = expected['oo_words'] != result['oo_words']
        if diff.any():
            print(f"\n{diff.sum()} differences found at positions:")
            print(diff[diff].index.tolist()[:20])  # Show first 20 differences
    else:
        print("\nExpected has:", expected['oo_words'].tolist())
        print("You have:", result['oo_words'].tolist())

    print("\n" + "=" * 70)
    print("\nWORDS_6PLUS COMPARISON:")
    print(f"Expected length: {len(expected['words_6plus'])}")
    print(f"Your length: {len(result['words_6plus'])}")
    print(f"Lengths match: {len(expected['words_6plus']) == len(result['words_6plus'])}")

    if len(expected['words_6plus']) == len(result['words_6plus']):
        print("\nFirst 10 expected:", expected['words_6plus'][:10].tolist())
        print("First 10 yours:", result['words_6plus'][:10].tolist())

        # check_shelve.py
        import shelve

        with shelve.open('expected_results') as exp:
            print("Keys in shelve:", list(exp.keys()))
            data = exp['analyzeWords']
            print("\nKeys in analyzeWords dict:", list(data.keys()))

            # Check the data types
            print(f"\noo_words type: {type(data['oo_words'])}")
            print(f"words_6plus type: {type(data['words_6plus'])}")

            # Check index types
            print(f"\noo_words index type: {type(data['oo_words'].index)}")
            print(f"words_6plus index type: {type(data['words_6plus'].index)}")

            # Check dtype
            print(f"\noo_words dtype: {data['oo_words'].dtype}")
            print(f"words_6plus dtype: {data['words_6plus'].dtype}")
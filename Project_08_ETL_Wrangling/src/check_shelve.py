# check_shelve.py
import shelve

with shelve.open('expected_results') as exp:
    print("Keys in shelve:", list(exp.keys()))
    data = exp['analyzeWords']
    print("\nKeys in analyzeWords dict:", list(data.keys()))

    # Check the Series properties
    print(f"\noo_words type: {type(data['oo_words'])}")
    print(f"oo_words dtype: {data['oo_words'].dtype}")
    print(f"oo_words index: {data['oo_words'].index[:5]}")

    print(f"\nwords_6plus type: {type(data['words_6plus'])}")
    print(f"words_6plus dtype: {data['words_6plus'].dtype}")
    print(f"words_6plus index: {data['words_6plus'].index[:5]}")

    # Check if there are any special attributes
    print(f"\noo_words name: {data['oo_words'].name}")
    print(f"words_6plus name: {data['words_6plus'].name}")
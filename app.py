from flask import Flask, request, jsonify
from flask_cors import CORS
from indic_transliteration.sanscript import transliterate, KANNADA, MALAYALAM, IAST, KOLKATA
import re

app = Flask(__name__)
CORS(app)  # Enable CORS

# Define the replacements for Latin to Kannada transliteration
replacements = [
    ('A', 'ā'), ('aa', 'ā'), ('I', 'ī'), ('ee', 'ī'), ('U', 'ū'),
    ('Ru', 'r̥'), ('oo', 'ū'), ('E', 'ē'), ('O', 'ō'), ('th', 't'), ('T', 'ṭ'),
    ('Th', 'ṭh'), ('D', 'ḍ'), ('Dh', 'ḍ'), ('N', 'ṇ'), ('sh', 'ś'),
    ('S', 'ś'), ('Sh', 'ṣ'), ('L', 'ḷ'), ("ae", "e್"), ("ch", "c"), ('ou', 'au'), ('x', 'ks'), ('w', 'v')
]

pattern = r'([aeiouAEIOU])([nNmM])([bcdfghjklpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ])'

def replace_nm(text):
    return re.sub(pattern, r'\1ṃ\3', text)

def replace_zero_with_n(text):
    # Replace all instances of '0' with 'ṃ' and 'l̤' with 'ḷ' in the text
    text = text.replace('0', 'ṃ')  # Replace '0' with 'ṃ'
    text = text.replace('l̤', 'ḷ')  # Replace 'l̤' with 'ḷ'
    return text

def apply_replacements(text):
    for old, new in replacements:
        text = text.replace(old, new)
    text = re.sub(pattern, r'\1ṃ\3', text)
    return text

def ae_replace(text):
    text = text.replace("ೆ್", "e")
    return text

# def J_replace(text):
    # text = text.replace("െ್", "J")
    # text = text.replace("െ്", "J")
    # return text

def J_replace(text):
    text = re.sub(r"(.{1})െ್", r"J\1", text)
    return text

def U_replace(text):
    text = re.sub(r"(.{1})െ്", r"J\1", text)
    return text

def period_replace(text):
    text = text.replace("।", ".")
    return text

def reverse_replacements(text):
    for old, new in replacements:
        text = text.replace(new, old)
    return text

@app.route('/transliterate', methods=['POST'])
def transliterate_text():
    data = request.json
    text = data.get('text')
    transliteration_type = data.get('type')

    if transliteration_type == 'kn_to_lat':
        text = ae_replace(text)
        text = transliterate(text, KANNADA, KOLKATA)
        transliterated_text = replace_zero_with_n(text)
    elif transliteration_type == 'kn_to_tu':
        transliterated_text = transliterate(text, KANNADA, MALAYALAM)
        transliterated_text = U_replace(transliterated_text)
    elif transliteration_type == 'lat_to_kn':
        # Apply the custom replacements
        text_with_replacements = apply_replacements(text)
        # Then transliterate the modified text using the KOLKATA scheme
        transliterated_text = transliterate(text_with_replacements, KOLKATA, KANNADA)
        transliterated_text = period_replace(transliterated_text)
    elif transliteration_type == 'lat_to_tu':
        text_with_replacements = apply_replacements(text)
        transliterated_text = transliterate(text_with_replacements, KOLKATA, MALAYALAM)
        transliterated_text = period_replace(transliterated_text)
        transliterated_text = J_replace(transliterated_text)
    elif transliteration_type == 'tu_to_kn':
        transliterated_text = transliterate(text, MALAYALAM, KANNADA)
    elif transliteration_type == 'tu_to_lat':
        text = transliterate(text, MALAYALAM, KOLKATA)
        transliterated_text = replace_zero_with_n(text)
    else:
        transliterated_text = 'Invalid transliteration type'

    return jsonify({'transliterated_text': transliterated_text})

if __name__ == '__main__':
    app.run(debug=True)



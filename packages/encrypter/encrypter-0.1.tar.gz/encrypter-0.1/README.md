# Encrypter

Encrypter is a module designed to convert characters into their corresponding numerical value, change it according to a randomly generated constant and finally turn them into characters again

## Installation

```python
pip install encrypter
```
## Usage

```python
import encrypter as enc

# create the Encrypter Object

encrypter_obj = enc.Encrypter()

text = "hello world"

# encrypt the message

ecrypted_text = encrypter_obj.encrypt(text)

#decrypt the message

decrypted_text = encrypter_obj.decrypt(encrypted_text)

```
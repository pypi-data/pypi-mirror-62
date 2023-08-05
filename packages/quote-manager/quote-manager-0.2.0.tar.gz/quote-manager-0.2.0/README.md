# library.quote.manager

Helper nlp library for handling non ascii quotes.

## Usage

```python3

from quote_manager import Quotes

sentence = “That’s an ‘magic’ shoe.”

ascii_quotes_sentence = Quotes(sentence)
# "That's an 'magic' shoe.'

# do stuff here...
ascii_quotes_transformed_sentence = transform(ascii_quotes_sentence)
# ex. grammar correction: "That's a 'magic' shoe.'

transformed_sentence = orignal_message.requote_modified_string(ascii_quotes_transformed_sentence)
# “That’s a ‘magic’ shoe.”
```
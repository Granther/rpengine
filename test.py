from groq import Groq
import os
import re
from dotenv import load_dotenv

text = "Hello how are you?"

text = text
text = re.sub("[.,:;?!]", "", text)

print(text)
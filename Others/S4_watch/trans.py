# -*- coding: utf-8 -*-
from google.cloud import translate
trans_text = "It is a beautiful day!"
trans_lang = "ja-JP"
def translate_text(text, trans_lang):
  if trans_lang == '':
    return text
  else:
    target_lang = trans_lang.split("-")[0]
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_lang)
    return result['translatedText']
  trans_result = translate_text(trans_text, trans_lang)
  print(trans_result)


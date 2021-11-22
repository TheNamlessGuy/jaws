import helpers.parser_tokenizer as tokenizer
import helpers.parser_processor as processor

def parse(str, uid):
  tokens = tokenizer.tokenize(str)
  return processor.process(tokens, uid)

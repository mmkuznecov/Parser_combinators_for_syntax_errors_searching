from parsy import generate, regex, string

# class for "while" expressions error checking

class WhileCheckCorr:
    
    def parse_obj(self, tokens):

        whitespace = regex(r'\s*')
        while_stmt = string('while')

        lexeme = lambda p: whitespace >> p << whitespace
        lbrace = lexeme(string('{'))
        rbrace = lexeme(string('}'))
        colon = lexeme(string(';'))
        
        cont = whitespace >> regex(r'\b(?:(?!while)\S)+\b') << whitespace
        
        content = (cont << colon | cont)

        while_obj = lbrace >> content.many() << rbrace
        while_ = while_stmt >> content.many() >> while_obj
        while_1 = whitespace >> while_ << whitespace
        full_make = (content.many() >> while_1 << content.many() | content.many() >> while_1)
        
        try:
            res = full_make.parse(tokens)
            return True
        except Exception as err:
            return err
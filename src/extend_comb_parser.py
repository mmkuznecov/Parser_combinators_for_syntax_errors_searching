from parsy import generate, regex, string

# class for "while" expressions error checking

class WhileCheckCorr:
    
    def parse_obj(self, tokens):

        whitespace = regex(r'\s*') #
        while_stmt = string('while')

        lexeme = lambda p: p << whitespace
        lbrace = lexeme(string('{'))
        rbrace = lexeme(string('}'))
        colon = lexeme(string(';'))

        cont = whitespace >> regex(r'\b(?:(?!while)\S)+\b') << whitespace
        
        content = (cont << colon | cont)

        # construct the parser

        while_obj = lbrace >> content.many() << rbrace
        make = whitespace >> while_obj << whitespace
        while_cond = content.many()
        while_ = while_stmt >> while_cond >> make
        contin = make << content.many()
        prev = (contin | content.many())
        while_1 = whitespace >> while_ << whitespace
        full_make = (prev >> while_1 << prev | prev >> while_1)
        
        try:
            res = full_make.parse(tokens)
            return True
        except Exception as err:
            return err
#include "Lexer.h"

Lexer::Lexer(const std::string & _input)
	:input(_input)
{
	c = (input.size() == 0) ? EOF : input[0];
}

void Lexer::consume()
{
	++p;
	c = (p >= input.size()) ? EOF : input[p];
}

void Lexer::match(char x)
{
	if (c == x) {
		consume();
	}
	else {
		throw Exception(std::string(1, c), std::string("expecting '") + x + "' found");
	}
}

Token ListLexer::Name()
{
	std::string temp;
	do {
		temp += c;
		consume();
	} while (isalpha(c));
	return Token(NAME, temp);
}

void ListLexer::WhiteSpace()
{
	while (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
		consume();
	}
}

ListLexer::ListLexer(const std::string & _input)
	:Lexer(_input)
{
}

Token ListLexer::nextToken()
{
	while (c != EOF) {
		switch (c)
		{
		case ' ': case '\t': case '\n': case '\r': WhiteSpace(); continue;
		case ',': consume(); return Token(COMMA, ",");
		case '[': consume(); return Token(LBRACK, "[");
		case ']': consume(); return Token(RBRACK, "]");
		default:
			if (isalpha(c)) {
				return Name();
			}
			else {
				throw Exception(std::string(1, c), "invalid character");
			}
		}
	}
	return Token(EOF_TYPE, "<EOF>");
}

std::string ListLexer::getTokenName(int type)
{
	return tokenNames[type];
}

LookaheadLexer::LookaheadLexer(const std::string & _input)
	:ListLexer(_input)
{
	tokenNames.push_back("EQUALS");
}

Token LookaheadLexer::nextToken()
{
	while (c != EOF) {
		switch (c)
		{
		case ' ': case '\t': case '\n': case '\r': WhiteSpace(); continue;
		case ',': consume(); return Token(COMMA, ",");
		case '[': consume(); return Token(LBRACK, "[");
		case ']': consume(); return Token(RBRACK, "]");
		case '=': consume(); return Token(EQUALS, "=");
		default:
			if (isalpha(c)) {
				return Name();
			}
			else {
				throw Exception(std::string(1, c), "invalid character");
			}
		}
	}
	return Token(EOF_TYPE, "<EOF>");
}

BacktrackLexer::BacktrackLexer(const std::string & _input)
	:LookaheadLexer(_input)
{
}

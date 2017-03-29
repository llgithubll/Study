#pragma once
#include <sstream>
#include <string>
#include <memory>
#include <stdexcept>
#include <ostream>
#include <vector>
#include <cctype>

#include "Utility.h"
#include "Token.h"

///////////////////////////////////////////////////////////////////////////////
//////						    Lexer(base)							     //////
///////////////////////////////////////////////////////////////////////////////
class Lexer {
protected:
	std::string input;
	std::string::size_type p = 0;		// index of current character
	char c;								// current character
public:
	enum {
		EOF_TYPE = 1
	};

	Lexer(const std::string& _input);
	void consume();
	void match(char x);
	virtual Token nextToken() = 0;
	virtual std::string getTokenName(int type) = 0;
	virtual ~Lexer() = default;
};
//=============================================================================
//ListLexer(derived)
class ListLexer : public Lexer {
protected:
	std::vector<std::string> tokenNames = {
		"n/a", "<EOF>", "NAME", "COMMA", "LBRACK", "RBRACK"
	};
	// NAME : [a-zA-Z]+ ; // consume the continuous alpha
	Token Name();
	// WhiteSpace : (' '|'\t'|'\n'|'\r')* ; // ignore all the whitespace
	void WhiteSpace();
public:
	enum {
		NAME = 2,
		COMMA = 3,
		LBRACK = 4,
		RBRACK = 5
	};

	ListLexer(const std::string& _input);
	Token nextToken() override;
	std::string getTokenName(int type) override;
};
//=============================================================================
//LookaheadLexer(derived)
class LookaheadLexer : public ListLexer {
public:
	enum {
		EQUALS = 6
	};

	LookaheadLexer(const std::string& _input);
	Token nextToken() override;
};
//=============================================================================
//BacktrackLexer(derived)
class BacktrackLexer : public LookaheadLexer {
	// this class is the same as super class
public:
	BacktrackLexer(const std::string& _input);
};



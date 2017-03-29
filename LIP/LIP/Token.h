#pragma once
#include <string>
#include <iostream>

///////////////////////////////////////////////////////////////////////////////
//////						    Token								     //////
///////////////////////////////////////////////////////////////////////////////
class Token {
public:
	int type;
	std::string text;
	Token() = default;
	Token(int _type, std::string _text);

	// toString
	std::string operator+(const std::string& other);
	operator std::string();
	std::string tostring();
};
// auxiliary Token's toString
std::string operator+(const std::string& str, Token& t);
std::ostream& operator<<(std::ostream& out, Token& t);

//=============================================================================
//VecMathToken
class VMToken : public Token {
public:
	enum {
		INVALID_TOKEN_TYPE = 0,
		PLUS = 1,
		MULT = 2,
		DOT = 3,
		INT = 4,
		VEC = 5,
		VAR = 6,
		ASSIGN = 7,
		PRINT = 8,
		STAT_LIST = 9
	};
	VMToken(int _type = 0, std::string _text = "")
		:Token(_type, _text) {}
};
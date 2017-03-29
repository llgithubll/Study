#include "Token.h"


Token::Token(int _type, std::string _text)
	:type(_type), text(_text)
{
}

std::string Token::operator+(const std::string & other)
{
	return (this->tostring() + other);
}

Token::operator std::string()
{
	return this->tostring();
}

std::string Token::tostring()
{
	return "<'" + text + "'," + std::to_string(type) + ">";
}

std::string operator+(const std::string & str, Token & t)
{
	return str + t.tostring();
}

std::ostream & operator<<(std::ostream & out, Token & t)
{
	out << t.tostring();
	return out;
}
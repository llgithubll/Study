#pragma once
#include <iterator>
#include <algorithm>
#include <vector>
#include <stack>
#include <unordered_map>
#include <iostream>
#include <cassert>
#include <stdexcept>
#include "Lexer.h"

///////////////////////////////////////////////////////////////////////////////
//////						    ParserLL1(base)							 //////
///////////////////////////////////////////////////////////////////////////////
class ParserLL1 {
protected:
	typedef std::unique_ptr<Lexer> UptrLexer;
	UptrLexer input;		// from where do we get tokens
	Token lookahead;
public:
	ParserLL1(UptrLexer _input);
	void match(int type);
	void consume();
};
//=============================================================================
//ListParserLL1(derived)
class ListParserLL1 : public ParserLL1 {
public:
	ListParserLL1(UptrLexer _input);
	// list : '[' elements ']' ; // match bracketed list
	void list();
	// elements : element (',' element)* ;
	void elements();
	// element : Name | list
	void element();
};

///////////////////////////////////////////////////////////////////////////////
//////						   ParserLLk(base) 						     //////
///////////////////////////////////////////////////////////////////////////////
class ParserLLk {
protected:
	typedef std::unique_ptr<Lexer> UptrLexer;
	UptrLexer input;
	std::vector<Token> lookahead;	// circular lookahead buffer
	int k;							// how many lookahead symbols
	int p = 0;						// circular index of next token position to fill
public:
	ParserLLk(UptrLexer _input, int _k);
	void consume();
	Token LT(int i);				// circular fetch
	int LA(int i);
	void match(int type);
};
//=============================================================================
//LookaheadParserLLk(derived)
class LookaheadParserLLk : public ParserLLk {
public:
	LookaheadParserLLk(UptrLexer _input, int _k);
	// list : '[' elements ']' ;
	void list();
	// elements : element (',' element)* ;
	void elements();
	// element : NAME '=' NAME | NAME | list ;
	void element();
};

///////////////////////////////////////////////////////////////////////////////
//////						   ParserBacktrack(base)				     //////
///////////////////////////////////////////////////////////////////////////////
class ParserBacktrack {
protected:
	typedef std::unique_ptr<Lexer> UptrLexer;
	UptrLexer input;
	std::stack<int> markers;		// stack of index markers into lookahead buffer
	std::vector<Token> lookahead;	// dynamically-sized lookahead buffer
	int p = 0;

	int mark();
	void release();
	void seek(int index);
	bool isSpeculating();
	
	void sync(int i);				// make sure we have i tokens from current position p
	void fill(int n);				// add n tokens
public:
	ParserBacktrack(UptrLexer _input);
	virtual void consume();
	Token LT(int i);	// lookahead i tokens(i > 0)
	int LA(int i);
	void match(int type);
};
//=============================================================================
//NaiveParserBacktrack(derived)
class NaiveParserBacktrack : public ParserBacktrack {
protected:
	bool speculate_stat_alt1();		// attempt alternative 1: list EOF
	bool speculate_stat_alt2();		// attempt alternative 2: assign EOF
public:
	NaiveParserBacktrack(UptrLexer _input);
	// stat : list EOF | assign EOF ;
	void stat();
	// assign : list '=' list ;
	void assign();
	// list : '[' elements ']' ;
	virtual void list();
	// elements : element (',' element) ;
	void elements();
	// element : NAME '=' NAME | NAME | list ;
	void element();
};

//=============================================================================
//MemoizeParserBacktrack(derived)
class MemoizeParserBacktrack : public NaiveParserBacktrack {
protected:
	static const int FAILED = -1;
	bool alreadyParsedRule(std::unordered_map<int, int> &m);
	void memoize(std::unordered_map<int, int> &m, int startTokenIndex, bool failed);
	int index();	// return current input position
	virtual void clearMemo() = 0;
public:
	MemoizeParserBacktrack(UptrLexer _input);
	void consume() override;
};
//=============================================================================
//AdvancedParserBacktrack(derived)
class AdvancedParserBacktrack : public MemoizeParserBacktrack {
private:
	std::unordered_map<int, int> list_memo;
	void _list();					// match '[' elements ']'
protected:
	void clearMemo() override;
public:
	AdvancedParserBacktrack(UptrLexer _input);
	void list() override;
};
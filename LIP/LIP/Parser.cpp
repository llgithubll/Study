#include "Parser.h"

ParserLL1::ParserLL1(UptrLexer _input)
	:input(std::move(_input))
{
	consume();
}

void ParserLL1::match(int type)
{
	if (lookahead.type == type) {
		consume();
	}
	else {
		throw Exception(lookahead.tostring(),
			std::string("expecting ") + input->getTokenName(type) + " found");
	}
}

void ParserLL1::consume()
{
	lookahead = input->nextToken();
}

ListParserLL1::ListParserLL1(UptrLexer _input)
	:ParserLL1(std::move(_input))
{
}

void ListParserLL1::list()
{
	match(ListLexer::LBRACK);
	elements();
	match(ListLexer::RBRACK);
}

void ListParserLL1::elements()
{
	element();
	while (lookahead.type == ListLexer::COMMA) {
		match(ListLexer::COMMA);
		element();
	}
}

void ListParserLL1::element()
{
	if (lookahead.type == ListLexer::NAME) {
		match(ListLexer::NAME);
	}
	else if (lookahead.type == ListLexer::LBRACK) {
		match(ListLexer::LBRACK);
	}
	else {
		throw Exception(lookahead.tostring(), "expecting name or list");
	}
}

ParserLLk::ParserLLk(UptrLexer _input, int _k)
	:input(std::move(_input)), k(_k)
{
	std::fill_n(std::back_inserter(lookahead), k, Token(0, "n/a"));	// lookahead buffer
	for (int i = 0; i < k; i++) {	// prime buffer with k lookahead
		consume();
	}
}

void ParserLLk::consume()
{
	lookahead[p] = input->nextToken();
	p = (p + 1) % k;
}

Token ParserLLk::LT(int i)
{
	return lookahead[(p + i - 1) % k];	// circular fetch
}

int ParserLLk::LA(int i)
{
	return LT(i).type;
}

void ParserLLk::match(int type)
{
	if (LA(1) == type) {
		consume();
	}
	else {
		throw Exception(LT(1), "expecting " + input->getTokenName(type));
	}
}

LookaheadParserLLk::LookaheadParserLLk(UptrLexer _input, int _k)
	:ParserLLk(std::move(_input), _k)
{
}

void LookaheadParserLLk::list()
{
	match(LookaheadLexer::LBRACK);
	elements();
	match(LookaheadLexer::RBRACK);
}

void LookaheadParserLLk::elements()
{
	element();
	while (LA(1) == LookaheadLexer::COMMA) {
		match(LookaheadLexer::COMMA);
		element();
	}
}

void LookaheadParserLLk::element()
{
	if (LA(1) == LookaheadLexer::NAME && LA(2) == LookaheadLexer::EQUALS) {
		match(LookaheadLexer::NAME);
		match(LookaheadLexer::EQUALS);
		match(LookaheadLexer::NAME);
	}
	else if (LA(1) == LookaheadLexer::NAME) {
		match(LookaheadLexer::NAME);
	}
	else if (LA(1) == LookaheadLexer::LBRACK) {
		list();
	}
	else {
		throw Exception(LT(1).tostring(), "expecting name or list");
	}
}

int ParserBacktrack::mark()
{
	markers.push(p);
	return p;
}

void ParserBacktrack::release()
{
	int marker = markers.top();
	markers.pop();
	seek(marker);
}

void ParserBacktrack::seek(int index)
{
	p = index;
}

bool ParserBacktrack::isSpeculating()
{
	return !markers.empty();
}

void ParserBacktrack::sync(int i)
{
	if ((p + i) > lookahead.size()) {
		int n = (p + i) - lookahead.size();
		fill(n);
	}
}

void ParserBacktrack::fill(int n)
{
	for (int i = 0; i < n; i++) {
		lookahead.push_back(input->nextToken());
	}
}

ParserBacktrack::ParserBacktrack(UptrLexer _input)
	:input(std::move(_input))
{
	sync(1);
}

void ParserBacktrack::consume()
{
	p++;
	// have we hit end of buffer when not backtracking
	if (p == lookahead.size() && !isSpeculating()) {
		p = 0;					// index can start 0 again(remain size)
	}
	sync(1);	// get another to replace consumed token
}

Token ParserBacktrack::LT(int i)
{
	if (i <= 0) {
		std::cerr << "lookahead negative or zeroth token is meaningless!" << std::endl;
		abort();
	}
	sync(i);
	return lookahead[p + i - 1];
}

int ParserBacktrack::LA(int i)
{
	return LT(i).type;
}

void ParserBacktrack::match(int type)
{
	if (LA(1) == type) {
		consume();
	}
	else {
		throw Exception(LT(1).tostring(), "excepting " + input->getTokenName(type) + " found");
	}
}

bool NaiveParserBacktrack::speculate_stat_alt1()
{
	bool success = true;
	mark();	// mark this spot in input so we can rewind
	try {
		list();
		match(BacktrackLexer::EOF_TYPE);
	}
	catch (Exception &e) {
		success = false;
	}
	release();	// either way, rewind to where we were
	return success;
}

bool NaiveParserBacktrack::speculate_stat_alt2()
{
	bool success = true;
	mark();
	try {
		assign();
		match(BacktrackLexer::EOF_TYPE);
	}
	catch (Exception &e) {
		success = false;
	}
	release();
	return success;
}

NaiveParserBacktrack::NaiveParserBacktrack(UptrLexer _input)
	:ParserBacktrack(std::move(_input))
{
}

void NaiveParserBacktrack::stat()
{
	if (speculate_stat_alt1()) {
		list();
		match(BacktrackLexer::EOF_TYPE);
	}
	else if (speculate_stat_alt2()) {
		assign();
		match(BacktrackLexer::EOF_TYPE);
	}
	else {
		throw Exception(std::string(""), "excepting stat found " + LT(1).tostring());
	}
}

void NaiveParserBacktrack::assign()
{
	try {
		list();
		match(BacktrackLexer::EQUALS);
		list();
	}
	catch (Exception &e) {
		throw;
	}
}

void NaiveParserBacktrack::list()
{
	try {
		match(BacktrackLexer::LBRACK);
		elements();
		match(BacktrackLexer::RBRACK);
	}
	catch (Exception &e) {
		throw;
	}
}

void NaiveParserBacktrack::elements()
{
	try {
		element();
		while (LA(1) == BacktrackLexer::COMMA) {
			match(BacktrackLexer::COMMA);
			element();
		}
	}
	catch (Exception &e) {
		throw;
	}
}

void NaiveParserBacktrack::element()
{
	try
	{
		if (LA(1) == BacktrackLexer::NAME && LA(2) == BacktrackLexer::EQUALS) {
			match(BacktrackLexer::NAME);
			match(BacktrackLexer::EQUALS);
			match(BacktrackLexer::NAME);
		}
		else if (LA(1) == BacktrackLexer::NAME) {
			match(BacktrackLexer::NAME);
		}
		else if (LA(1) == BacktrackLexer::LBRACK) {
			list();
		}
		else {
			throw Exception("", "excepting element found " + LT(1).tostring());
		}
	}
	catch (Exception &e)
	{
		throw;
	}
}

bool MemoizeParserBacktrack::alreadyParsedRule(std::unordered_map<int, int>& m)
{
	int memoI;
	try {
		memoI = m.at(index());
	}
	catch (std::out_of_range &e) {
		return false;
	}

	if (memoI == FAILED) {
		throw Exception("", "previous parse failed");
	}
	else {
		std::cout << "parsed list before at index " << index()
			<< " ;skip ahead to token index " << memoI
			<< ": " << lookahead[memoI].text << std::endl;
		seek(memoI);
	}
	return true;
}

void MemoizeParserBacktrack::memoize(std::unordered_map<int, int>& m, int startTokenIndex, bool failed)
{
	int stopTokenIndex = failed ? FAILED : index();
	m[startTokenIndex] = stopTokenIndex;
}

int MemoizeParserBacktrack::index()
{
	return p;
}


MemoizeParserBacktrack::MemoizeParserBacktrack(UptrLexer _input)
	:NaiveParserBacktrack(std::move(_input))
{
}

void MemoizeParserBacktrack::consume()
{
	p++;
	// we hit end of buffer when not backtracking
	if (p == lookahead.size() && !isSpeculating()) {
		p = 0;
		clearMemo();	// clear any rule memorized dictionaies
	}
	sync(1);
}


void AdvancedParserBacktrack::_list()
{
	std::cout << "parse list rule at token index:" << index() << std::endl;
	match(BacktrackLexer::LBRACK);
	elements();
	match(BacktrackLexer::RBRACK);
}


void AdvancedParserBacktrack::clearMemo()
{
	list_memo.clear();
}

AdvancedParserBacktrack::AdvancedParserBacktrack(UptrLexer _input)
	:MemoizeParserBacktrack(std::move(_input))
{
}


void AdvancedParserBacktrack::list()
{
	bool failed = false;
	int startTokenIndex = index();
	if (isSpeculating() && alreadyParsedRule(list_memo)) {
		return;
	}

	try {
		_list();
	}
	catch (Exception &e) {
		failed = true;
		if (isSpeculating()) {
			memoize(list_memo, startTokenIndex, failed);
		}
		throw;
	}

	if (isSpeculating()) {
		memoize(list_memo, startTokenIndex, failed);
	}
}


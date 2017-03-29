#include <iostream>
#include <cassert>
#include <vector>
#include <string>
#include "Lexer.h"
#include "Parser.h"
#include "AST.h"

using namespace std;

int main() {
	{ // Token
		cout << "*******Token*******" << endl;
		Token t(-2, "test");
		assert(t.type == -2);
		assert(t.text == "test");
		assert(t.tostring() == "<'test',-2>");
		assert("token:" + t == "token:<'test',-2>");
	}
	{ // ListLexer
		cout << "*******ListLexer*******" << endl;
		string input = "[a, b , c ]";
		ListLexer lexer(input);
		Token t = lexer.nextToken();
		while (t.type != ListLexer::EOF_TYPE) {
			cout << t << "\t"<< lexer.getTokenName(t.type) << endl;
			t = lexer.nextToken();
		}
		cout << t << "\t" << lexer.getTokenName(t.type) << endl;
	}
	{ // ListParserLL1
		cout << "*******ListParserLL1*******" << endl;
		try {
			unique_ptr<Lexer> lexer = make_unique<ListLexer>("a, b]");
			ListParserLL1 parserll1(std::move(lexer));
			parserll1.list();
		}
		catch (Exception &e) {
			cout << e.context << ":" << e.error << endl;
		}
	}
	{ // LookaheadParserLLk
		cout << "*******LookaheadParserLLk*******" << endl;
		try {
			unique_ptr<Lexer> lexer = make_unique<LookaheadLexer>("[a, b==c, [d, e]]");
			LookaheadParserLLk parserllk(std::move(lexer), 2);
			parserllk.list();
		}
		catch (Exception &e) {
			cout << e.context << ":" << e.error << endl;
		}
	}
	{ // NaiveParserBacktrack
		cout << "*******NaiveParserBacktrack*******" << endl;
		try {
			unique_ptr<Lexer> lexer = make_unique<BacktrackLexer>("[a, b] = [c, d]");
			NaiveParserBacktrack parser(std::move(lexer));
			//cout << parser.LT(11) << endl;	// lookahead far
			parser.stat();
		}
		catch (Exception &e) {
			cout << e.context << ":" << e.error << endl;
		}
	}
	{ // AdvancedParserBacktrack
		cout << "*******AdvancedParserBacktrack*******" << endl;
		try {
			unique_ptr<Lexer> lexer = make_unique<BacktrackLexer>("[a, b] = [c, d]");
			AdvancedParserBacktrack parser(std::move(lexer));
			parser.stat();
		}
		catch (Exception &e) {
			cout << e.context << ":" << e.error << endl;
		}

	}
	{ // AST & NormalizedAST
		enum {
			INVLID = 0,
			PLUS = 1,
			MINU = 2,
			MUL = 3,
			DIV = 4,
			INT = 5,
			VEC = 6
		};
		{ // AST
			cout << "*******AST*******" << endl;
			AST root(MUL, "*");
			AST plus(PLUS, "+");
			plus.addChild(AST(INT, "1"));
			plus.addChild(AST(INT, "2"));
			plus.addChild(AST(INT, "3"));
			AST minu(MINU, "-");
			minu.addChild(AST(INT, "4"));
			minu.addChild(AST(INT, "5"));
			root.addChild(plus);
			root.addChild(minu);
			root.printTree();
			cout << endl;
		}
		{ // NormalizedAST
			cout << "*******NormalizedAST*******" << endl;
			Token plus(PLUS, "+");
			Token one(INT, "1");
			Token two(INT, "2");
			AddNode root(IntNode(one), plus, IntNode(two));
			root.printTree();
			cout << endl;
			IntNode(one).printNode();
			cout << endl;
			vector<ExprNode> ve = { root, IntNode(one), IntNode(two) };
			VectorNode vn(Token(VEC, "VectorNode"), ve);
			vn.printTree();
			cout << endl;
			vn.printNode();
			cout << endl;
		}
		{ // HeteroAST
			cout << "*******HeteroAST*******" << endl;
			Token plus(PLUS, "+");
			Token one(INT, "1");
			Token two(INT, "2");
			HeteroAddNode root(HeteroIntNode(one), plus, HeteroIntNode(two));
			root.printTree();
			cout << endl;
			HeteroIntNode(one).printNode();
			cout << endl;
		}
	}
	{ // VecMath
		cout << "*******VecMath*******" << endl;
#define I(num) VMIntNode(VMToken(VMToken::INT, to_string(num)))
		PrintVisitor visitor;
		visitor.print(I(3));	cout << endl;
		
		VMToken tplus(VMToken::PLUS, "+");
		VMIntNode i3(VMToken(VMToken::INT, to_string(3)));
		VMIntNode i4(VMToken(VMToken::INT, to_string(4)));
		auto SpI3 = make_shared<VMIntNode>(i3);
		auto SpI4 = make_shared<VMIntNode>(i4);
		VMAddNode a(SpI3, tplus, SpI4);
		visitor.print(a);	cout << endl;

		VMAddNode a2(make_shared<VMIntNode>(I(9)), tplus, make_shared<VMIntNode>(I(9)));
		visitor.print(a2);	cout << endl;

		VMToken tvar(VMToken::VAR, "x");
		VMVarNode var(tvar);
		visitor.print(var);	cout << endl;
		VMToken tass(VMToken::ASSIGN, "=");
		VMAssignNode assign(make_shared<VMVarNode>(var), tass, make_shared<VMAddNode>(a));
		visitor.print(assign);

		VMPrintNode pn(VMToken(VMToken::PRINT), make_shared<VMAddNode>(a));
		visitor.print(pn);

		VMDotProductNode dp(SpI3, VMToken(VMToken::DOT),SpI4);
		visitor.print(dp); cout << endl;
		VMMulNode m(SpI3, VMToken(VMToken::MULT), SpI4);
		visitor.print(m); cout << endl;

		vector<shared_ptr<VMExprNode>> v1 = { SpI3, SpI4 };
		vector<shared_ptr<VMExprNode>> v2 = { SpI4, SpI3 };
		VMVectorNode vn1(VMToken(VMToken::VEC), v1);
		visitor.print(vn1); cout << endl;
		VMVectorNode vn2(VMToken(VMToken::VEC), v2);
		VMMulNode vm(make_shared<VMVectorNode>(vn1), VMToken(VMToken::MULT), make_shared<VMVectorNode>(vn2));
		visitor.print(vm); cout << endl;

		vector<shared_ptr<VMStatNode>> vs = 
			{ make_shared<VMAssignNode>(assign), make_shared<VMPrintNode>(pn) };
		VMStatListNode sl(vs);
		visitor.print(sl);
	}
	cout << "\n\nSUCCESS" << endl;
	system("pause");
	return 0;
}
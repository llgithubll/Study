#include "AST.h"

AST::AST()
{
	token.text = "nil";
}

AST::AST(const Token & t)
{
	token = t;
}

AST::AST(int _type, std::string _text)
{
	token = Token(_type, _text);
}

int AST::getNodeType()
{
	return token.type;
}

void AST::addChild(AST t)
{
	children.push_back(t);
}

void AST::printNode()
{
	std::cout << token.text;
}

void AST::printTree()
{
	if (children.size() == 0) {
		std::cout << token.text;
	}
	else {
		std::cout << "(" << token.text;
		for (int i = 0; i < children.size(); i++) {
			std::cout << " ";
			children[i].printTree();
		}
		std::cout << ")";
	}
}

ExprNode::ExprNode(Token & t)
	:AST(t)
{
}

ExprNode::ExprNode(AST & _ast)
	:AST(_ast)
{
}


void ExprNode::printNode()
{
	if (evalType != INVALID) {
		AST::printNode();
		std::cout << "<type=" << (evalType == INTEGER ? "INTEGER" : "VECTOR") << ">";
	}
	else {
		AST::printNode();
	}
}

AddNode::AddNode(ExprNode & _left, Token & _t, ExprNode & _right)
	:ExprNode(_t)
{
	addChild(_left);
	addChild(_right);
}


IntNode::IntNode(Token & _t)
	:ExprNode(_t)
{
	evalType = INTEGER;
}

VectorNode::VectorNode(Token & _t, std::vector<ExprNode>& _elements)
	:ExprNode(_t)
{
	evalType = VECTOR;
	for (ExprNode &e : _elements) {
		addChild(e);
	}
}

HeteroAST::HeteroAST()
{
	token.text = "nil";
}

HeteroAST::HeteroAST(const Token & t)
{
	token = t;
}

HeteroAST::HeteroAST(int _type, std::string _text)
{
	token = Token(_type, _text);
}

void HeteroAST::printNode()
{
	std::cout << token.text;
}

void HeteroAST::printTree()
{
	printNode();
}

HeteroExprNode::HeteroExprNode(Token & _t)
	:HeteroAST(_t)
{
}

HeteroAddNode::HeteroAddNode(HeteroExprNode & _left, Token & _add, HeteroExprNode & _right)
	:HeteroExprNode(_add)
{
	left = _left;
	right = _right;
}

void HeteroAddNode::printTree()
{
	std::cout << "(" << token.text << " ";
	left.printTree();
	std::cout << " ";
	right.printTree();
	std::cout << ")";
}

HeteroIntNode::HeteroIntNode(Token & _t)
	:HeteroExprNode(_t)
{
}


HeteroVectorNode::HeteroVectorNode(Token & _t, std::vector<HeteroExprNode>& _elements)
	:HeteroExprNode(_t)
{
	elements = _elements;
}

void HeteroVectorNode::printTree()
{
	if (elements.size() == 0) {
		printNode();
	}
	else {
		for (int i = 0; i < elements.size(); i++) {
			if (i > 0) {
				std::cout << " ";
			}
			else {
				elements[i].printTree();
			}
		}
	}
}

void PrintVisitor::print(const VMAST & _n)
{
	switch (_n.token.type)
	{
	case VMToken::VAR:		print(dynamic_cast<const VMVarNode&>(_n)); break;
	case VMToken::INT:		print(dynamic_cast<const VMIntNode&>(_n)); break;
	case VMToken::PLUS:		print(dynamic_cast<const VMAddNode&>(_n)); break;
	case VMToken::ASSIGN:	print(dynamic_cast<const VMAssignNode&>(_n)); break;
	case VMToken::PRINT:	print(dynamic_cast<const VMPrintNode&>(_n)); break;
	case VMToken::MULT:		print(dynamic_cast<const VMMulNode&>(_n)); break;
	case VMToken::DOT:		print(dynamic_cast<const VMDotProductNode&>(_n)); break;
	case VMToken::VEC:		print(dynamic_cast<const VMVectorNode&>(_n)); break;
	case VMToken::STAT_LIST:print(dynamic_cast<const VMStatListNode&>(_n)); break;
	default:
		std::cout << "cannot handle this token.type:" 
			<< _n.token.type << std::endl;
		break;
	}
}

void PrintVisitor::print(const VMIntNode & _n)
{
	std::cout << _n.token.text;
}

void PrintVisitor::print(const VMVarNode & _n)
{
	std::cout << _n.token.text;
}

void PrintVisitor::print(const VMAddNode & _n)
{
	print(*_n.left);
	std::cout << "+";
	print(*_n.right);
}

void PrintVisitor::print(const VMAssignNode & _n)
{
	print(*_n.var);
	std::cout << "=";
	print(*_n.value);
	std::cout << std::endl;
}

void PrintVisitor::print(const VMPrintNode & _n)
{
	std::cout << "print ";
	print(*_n.value);
	std::cout << std::endl;
}

void PrintVisitor::print(const VMMulNode & _n)
{
	print(*_n.left);
	std::cout << "*";
	print(*_n.right);
}

void PrintVisitor::print(const VMDotProductNode & _n)
{
	print(*_n.left);
	std::cout << ".";
	print(*_n.right);
}

void PrintVisitor::print(const VMVectorNode & _n)
{
	std::cout << "[";
	for (int i = 0; i < _n.elements.size(); i++) {
		if (i > 0) {
			std::cout << ",";
		}
		print(*_n.elements[i]);
	}
	std::cout << "]";
}

void PrintVisitor::print(const VMStatListNode & _n)
{
	for (auto &e : _n.elements) {
		print(*e);
	}
}

void VMIntNode::print()
{
	std::cout << token.text;
}

void VMAddNode::print()
{
	left->print();
	std::cout << "+";
	right->print();
}

void VMAssignNode::print()
{
	var->print();
	std::cout << "=";
	value->print();
}

void VMVarNode::print()
{
	std::cout << token.text;
}

void VMPrintNode::print()
{
	std::cout << "print ";
	value->print();
}

void VMMulNode::print()
{
	left->print();
	std::cout << "*";
	right->print();
}

void VMDotProductNode::print()
{
	left->print();
	std::cout << ".";
	right->print();
}

void VMVectorNode::print()
{
	std::cout << "[";
	for (int i = 0; i < elements.size(); i++) {
		if (i > 0) {
			std::cout << ",";
		}
		elements[i]->print();
	}
	std::cout << "]";
}

void VMStatListNode::print()
{
	for (auto &e : elements) {
		e->print();
	}
}

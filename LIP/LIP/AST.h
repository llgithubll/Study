#include <vector>
#include <iostream>
#include <string>
#include <memory>
#include "Token.h"

///////////////////////////////////////////////////////////////////////////////
//////						    (homogeneous)AST					     //////
///////////////////////////////////////////////////////////////////////////////
class AST {
public:
	Token token;
	std::vector<AST> children;

	AST();	// empty root AST is a list
	AST(const Token &t);
	AST(int _type, std::string _text);

	int getNodeType();
	void addChild(AST t);

	virtual void printNode();
	void printTree();
};

//=============================================================================
//(normalized)ExprNode
class ExprNode : public AST {
protected:
	int evalType = INVALID;
public:
	enum {
		INVALID = 0,
		INTEGER = 1,
		VECTOR = 2
	};

	ExprNode(Token &t);
	ExprNode(AST &_ast);
	void printNode() override;
};

//=============================================================================
//(normalized)AddNode
class AddNode : public ExprNode {
public:
	AddNode(ExprNode &_left, Token &_t, ExprNode &_right);
};

//=============================================================================
//(normalized)IntNode
class IntNode : public ExprNode {
public:
	IntNode(Token &_t);
};

//=============================================================================
//(normalized)VectorNode
class VectorNode : public ExprNode {
public:
	VectorNode(Token &_t, std::vector<ExprNode> &_elements);
};



///////////////////////////////////////////////////////////////////////////////
//////						    (heterodox)HeteroAST				     //////
///////////////////////////////////////////////////////////////////////////////
class HeteroAST {
public:
	Token token;

	HeteroAST();
	HeteroAST(const Token &t);
	HeteroAST(int _type, std::string _text);

	void printNode();
	virtual void printTree();
};

//=============================================================================
//HeteroExprNode
class HeteroExprNode : public HeteroAST {
public:
	HeteroExprNode() = default;
	HeteroExprNode(Token &_t);
};

//=============================================================================
//HeteroAddNode
class HeteroAddNode : public HeteroExprNode {
public:
	HeteroAddNode(HeteroExprNode &_left, Token &_add, HeteroExprNode &_right);
	void printTree() override;
private:
	HeteroExprNode left, right;
};

//=============================================================================
//HeteroIntNode
class HeteroIntNode : public HeteroExprNode {
public:
	HeteroIntNode(Token &_t);
};

//=============================================================================
//HeteroVectorNode
class HeteroVectorNode : public HeteroExprNode {
private:
	std::vector<HeteroExprNode> elements;
public:
	HeteroVectorNode(Token &_t, std::vector<HeteroExprNode> &_elements);
	void printTree() override;
};

///////////////////////////////////////////////////////////////////////////////
//////						    VM(VecMath)								 //////
///////////////////////////////////////////////////////////////////////////////
// VecMath is a hetero AST
class VMAST {
public:
	VMToken token;
	VMAST() :token(VMToken(VMToken::INVALID_TOKEN_TYPE)) {}
	VMAST(const VMToken &_t) :token(_t) {}
	~VMAST() = default;
	virtual void print() = 0;
};

class VMExprNode : public VMAST {
public:
	VMExprNode() :VMAST() {}
	VMExprNode(const VMToken &_t) :VMAST(_t) {}
	virtual void print() = 0;
};

class VMIntNode : public VMExprNode {
public:
	VMIntNode() { token.type = VMToken::INT; }
	VMIntNode(const VMToken &_t) :VMExprNode(_t) {}
	virtual void print() override;
};

class VMVarNode : public VMExprNode {
public:
	VMVarNode(const VMToken &_t) :VMExprNode(_t) {}
	virtual void print() override;
};

class PrintVisitor;
class VMAddNode : public VMExprNode {
	friend class PrintVisitor;
private:
	typedef std::shared_ptr<VMExprNode> SpExpr;
	SpExpr left, right;
public:
	VMAddNode(SpExpr _left, const VMToken &_t, SpExpr _right)
		:left(_left), VMExprNode(_t), right(_right) {}
	virtual void print() override;
};

class VMMulNode : public VMExprNode {
	friend class PrintVisitor;
private:
	typedef std::shared_ptr<VMExprNode> SpExpr;
	SpExpr left, right;
public:
	VMMulNode(SpExpr _left, const VMToken &_t, SpExpr _right)
		:left(_left), VMExprNode(_t), right(_right) {}
	virtual void print() override;
};

class VMDotProductNode : public VMExprNode {
	friend class PrintVisitor;
private:
	typedef std::shared_ptr<VMExprNode> SpExpr;
	SpExpr left, right;
public:
	VMDotProductNode(SpExpr _left, const VMToken &_t, SpExpr _right)
		:left(_left), VMExprNode(_t), right(_right) {}
	virtual void print() override;
};

class VMVectorNode : public VMExprNode {
	friend class PrintVisitor;
private:
	typedef std::shared_ptr<VMExprNode> SpExpr;
	std::vector<SpExpr> elements;
public:
	VMVectorNode(const VMToken &_t, std::vector<SpExpr> &_elements)
		:VMExprNode(_t), elements(_elements) {}
	virtual void print() override;
};

class VMStatNode : public VMAST {
public:
	VMStatNode() :VMAST() {}
	VMStatNode(const VMToken &_t) :VMAST(_t) {}
	virtual void print() = 0;
};

class VMAssignNode : public VMStatNode {
	friend class PrintVisitor;
private:
	std::shared_ptr<VMVarNode> var;
	std::shared_ptr<VMExprNode> value;
public:
	VMAssignNode(std::shared_ptr<VMVarNode> _var,
		const VMToken &_t, std::shared_ptr<VMExprNode> _value)
		:var(_var), VMStatNode(_t), value(_value) {}
	virtual void print() override;
};

class VMPrintNode : public VMStatNode {
	friend class PrintVisitor;
private:
	std::shared_ptr<VMExprNode> value;
public:
	VMPrintNode(const VMToken &_t, std::shared_ptr<VMExprNode> _value)
		:VMStatNode(_t), value(_value) {}
	virtual void print() override;
};

class VMStatListNode : public VMAST {
	friend class PrintVisitor;
private:
	typedef std::shared_ptr<VMStatNode> SpSt;
	std::vector<SpSt> elements;
public:
	VMStatListNode(std::vector<SpSt> &_elements)
		:VMAST(VMToken(VMToken::STAT_LIST)), elements(_elements) {}
	virtual void print() override;
};

class PrintVisitor {
public:
	void print(const VMAST &_n);
	void print(const VMIntNode &_n);
	void print(const VMVarNode &_n);
	void print(const VMAddNode &_n);
	void print(const VMAssignNode &_n);
	void print(const VMPrintNode &_n);
	void print(const VMMulNode &_n);
	void print(const VMDotProductNode &_n);
	void print(const VMVectorNode &_n);
	void print(const VMStatListNode &_n);
};
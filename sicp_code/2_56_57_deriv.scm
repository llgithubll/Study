;;variable
(define (variable? x) (symbol? x))

(define (same-variable? v1 v2)
    (and (variable? v1) (variable? v2) (eq? v1 v2)))

(define (=number? exp num)
    (and (number? exp) (= exp num)))

; accumulate the result of the first and the already accumulated
(define (accumulate op initial sequence)
    (if (null? sequence)
        initial
        (op (car sequence)
            (accumulate op initial (cdr sequence)))))

;;sum
(define (sum? x)
    (and (pair? x) (eq? (car x) '+)))

(define (addend s) (cadr s))

;(define (augend s) (caddr s))
(define (augend s)
    (accumulate make-sum 0 (cddr s)))

(define (make-sum a1 a2)
    (cond ((=number? a1 0) a2)
            ((=number? a2 0) a1)
            ((and (number? a1) (number? a2)) (+ a1 a2))
            (else (list '+ a1 a2))))


;;product
(define (product? x)
    (and (pair? x) (eq? (car x) '*)))

(define (multiplier p) (cadr p))

; (define (multiplicand p) (caddr p))
(define (multiplicand p)
    (accumulate make-product 1 (cddr P)))

(define (make-product m1 m2)
    (cond ((or (=number? m1 0) (=number? m2 0)) 0)
            ((=number? m1 1) m2)
            ((=number? m2 1) m1)
            ((and (number? m1) (number? m2)) (* m1 m2))
            (else (list '* m1 m2))))


;;exponentiation
(define (exponentiation? x)
    (and (pair? x) (eq? (car x) '**)))

(define (base e) (cadr e))

(define (exponent e) (caddr e))

(define (expt b n)
    (if (= n 0) 1 (* b (expt b (- n 1)))))

(define (make-exponentiation b e)
    (cond ((=number? e 0) 1)
            ((=number? e 1) b)
            ((and (number? b) (number? e)) (expt b e))
            (else (list '** b e))))


;;deriv
(define (deriv exp var)
    (cond ((number? exp) 0)
            ((variable? exp) (if (same-variable? exp var) 1 0))
            ((sum? exp)
                (make-sum (deriv (addend exp) var)
                            (deriv (augend exp) var)))
            ((product? exp)
                (make-sum
                    (make-product (multiplier exp)
                                    (deriv (multiplicand exp) var))
                    (make-product (deriv (multiplier exp) var)
                                    (multiplicand exp))))
            ((exponentiation? exp)
                (make-product (make-product (exponent exp)
                                            (make-exponentiation (base exp)
                                                                    (- (exponent exp) 1)))
                                (deriv (base exp) var)))))
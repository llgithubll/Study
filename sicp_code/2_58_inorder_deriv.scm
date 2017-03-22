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
    (and (pair? x) (eq? (cadr x) '+)))

(define (addend s)
    (car s))

(define (augend s)
    (accumulate make-sum 0 (cddr s)))

(define (make-sum a1 a2)
    (cond ((=number? a1 0) a2)
            ((=number? a2 0) a1)
            ((and (number? a1) (number? a2)) (+ a1 a2))
            (else (list a1 '+ a2))))





;;deriv(only for sum)
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
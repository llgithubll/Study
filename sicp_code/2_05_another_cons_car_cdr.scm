; helper
(define (count-0-remainder-divisions n divisor)
    (define (iter try-exp)
        (if (= 0 (remainder n (expt divisor try-exp)))
            (iter (+ try-exp 1))
            (- try-exp 1)))
    (iter 1))

(define (my-cons a b) (* (expt 2 a) (expt 3 b)))
(define (my-car z) (count-0-remainder-divisions z 2))
(define (my-cdr z) (count-0-remainder-divisions z 3))

(define pair (my-cons 3 2))

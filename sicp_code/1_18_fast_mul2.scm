(define (fast-mul a b)
    (define (double x) (+ x x))
    (define (halve x) (/ x 2))
    (define (even? x) (= (remainder x 2) 0))

    (define (helper a b product)
        (cond ((= b 0) product)
            ((even? b) (helper (double a) (halve b) product))
            (else (helper a (- b 1) (+ a product)))))
    (helper a b 0))

(fast-mul 3 10)

    
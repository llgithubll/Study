(define (smallest-divisor n)
    (find-divisor n 2))

(define (find-divisor n test-divisor)
    (define (next test-divisor) ;ex-1-23
        (if (= test-divisor 2) 3 (+ test-divisor 1)))
    (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (next test-divisor)))))

(define (divides? a b) (= (remainder b a) 0))

(smallest-divisor 199)
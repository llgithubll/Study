; filtered-accumulate
(define (filtered-accumulate combiner null-value term a next b filter)
    (define (iter a result)
        (cond ((> a b) result)
            ((filter a) (iter (next a) (combiner result (term a))))
            (else (iter (next a) result))))
    (iter a null-value))

(define (identity x) x)
(define (inc x) (+ x 1))

; prime?
(define (smallest-divisor n)
    (find-divisor n 2))

(define (find-divisor n test-divisor)
    (cond ((> (square test-divisor) n) n)
        ((divides? test-divisor n) test-divisor)
        (else (find-divisor n (+ test-divisor 1)))))

(define (divides? a b) (= (remainder b a) 0))

(define (prime? n)
    (if (= n 1)
        false
        (= n (smallest-divisor n))))

; sum-of-primes
(define (sum-of-primes a b)
    (filtered-accumulate + 0 identity a inc b prime?))

(sum-of-primes 1 5)

; gcd, relative-prime
(define (gcd m n)
    (cond ((< m n) (gcd n m))
        ((= n 0) m)
        (else (gcd n (remainder m n)))))

(define (relative-prime? m n)
    (= (gcd m n) 1))

(define (product-of-relative-prime n)
    (define (filter x)
        (relative-prime? x n))
    (filtered-accumulate * 1 identity 1 inc n filter))

(product-of-relative-prime 10)

; product-of-relative-prime

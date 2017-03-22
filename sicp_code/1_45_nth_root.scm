; average-damp
(define (average x y) (/ (+ x y) 2.0))
(define (average-damp f)
    (lambda (x) (average x (f x))))

; fixed-point
(define tolerance 0.00001)

(define (fixed-point f first-guess)
    (define (close-enough? v1 v2)
        (< (abs (- v1 v2)) tolerance))
    (define (try guess)
        (newline)
        (display guess)
        (let ((next (f guess)))
            (if (close-enough? guess next)
                next
                (try next))))
    (try first-guess))

; repeated
(define (compose f g)
    (lambda (x)
        (f (g x))))

(define (repeated f times)
    (if (< times 1)
        (lambda (x) x)
        (compose f (repeated f (- times 1)))))

; pow
(define (pow b n)
    (define (iter a b n)
        (cond ((= n 0) a)
            ((even? n) (iter a (square b) (/ n 2)))
            (else (iter (* a b) b (- n 1)))))
    (iter 1 b n))

(define (even? n)
    (= (remainder n 2) 0))

(define (square n)
    (* n n))

; nth-root
(define (log2 x) (/ (log x) (log 2)))
(define (nth-root n x)
    (fixed-point ((repeated average-damp (floor (log2 n)))
                        (lambda (y) (/ x (pow y (- n 1)))))
                    1.0))

(nth-root 5 32)
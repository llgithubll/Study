(define (compose f g)
    (lambda (x)
        (f (g x))))

(define (repeated f times)
    (if (< times 1)
        (lambda (x) x)
        (compose f (repeated f (- times 1)))))

(define (square i) (* i i))
((repeated square 2) 5)


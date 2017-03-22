(define (f g)
    (g 2))

(f (lambda (z) (* z (+ z 1))))
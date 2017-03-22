(define (equal? a b)
    (cond ((and (null? a) (null? b)) #t)
            ((and (pair? a) (pair? b)) (and (equal? (car a) (car b)) (equal? (cdr a) (cdr b))))
            ((eq? a b) #t)
            (else #f)))
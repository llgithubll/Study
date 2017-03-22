(define (same-parity first . other)
    (define (iter items result)
        (if (null? items)
            result
            (if (= (remainder first 2) (remainder (car items) 2))
                    (iter (cdr items) (append result (list (car items))))
                    (iter (cdr items) result))))
    (iter other ()))

(define (reverse items)
    (define (iter list1 list2)
        (if (null? list1)
            list2
            (iter (cdr list1) (cons (car list1) list2))))
    (iter items ()))

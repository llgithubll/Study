; Supporting functions
(define (filter predicate sequence)
    (cond ((null? sequence) ())
            ((predicate (car sequence))
                (cons (car sequence)
                        (filter predicate (cdr sequence))))
            (else (filter predicate (cdr sequence)))))

(define (accumulate op initial sequence)
    (if (null? sequence)
        initial
        (op (car sequence)
            (accumulate op initial (cdr sequence)))))

(define (enumerate-interval low high)
    (if (> low high)
        ()
        (cons low (enumerate-interval (+ low 1) high))))

(define (flatmap proc seq)
    (accumulate append () (map proc seq)))

;
(define (ordered-triples-sum n s)
    (filter (lambda (list) (= (accumulate + 0 list) s))
        (flatmap (lambda (i)
            (flatmap (lambda (j)
                (map (lambda (k) (list i j k))
                    (enumerate-interval 1 (- j 1))))
                (enumerate-interval 1 (- i 1))))
            (enumerate-interval 1 n))))                             
            
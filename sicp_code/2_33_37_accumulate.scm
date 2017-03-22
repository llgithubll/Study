; accumulate the result of the first and the already accumulated
(define (accumulate op initial sequence)
    (if (null? sequence)
        initial
        (op (car sequence)
            (accumulate op initial (cdr sequence)))))

; map
(define (my-map proc sequence)
    (accumulate (lambda (first already-accumulated)
                        (cons (proc first) already-accumulated))
                ()
                sequence))
; append
(define (append list1 list2)
    (accumulate cons list2 list1))
; length
(define (length sequence)
    (accumulate (lambda (first already-acc) (+ 1 already-acc))
                0
                sequence))

; horner
(define (horner-eval x coefficient-sequence)
    (accumulate (lambda (this-coeff higher-terms)
                        (+ (* higher-terms x) this-coeff))
                0
                coefficient-sequence))

; count-leaves
(define (count-leaves t)
    (accumulate +
                0
                (my-map (lambda (node)
                        (if (pair? node)
                            (count-leaves node)
                            1))
                    t)))

; accumulate-n                                    
(define (accumulate-n op init seqs)
    (if (null? (car seqs))
        ()
        (cons (accumulate op init (my-map car seqs))
                (accumulate-n op init (my-map cdr seqs)))))
                                                
; matrix
(define matrix (list (list 1 2 3 4) (list 5 6 7 8) (list 9 10 11 12)))

(define (dot-product v w)
    (accumulate + 0 (map * v w)))

(define (matrix-*-vector m v)
    (map (lambda (m-row) (dot-product m-row v)) m))

(define (transpose mat)
    (accumulate-n cons () mat))

(define (matrix-*-matrix m n)
    (let ((n-cols (transpose n)))
        (map (lambda (m-row)
                        (map (lambda (n-col) (dot-product m-row n-col)) n-cols))
                m)))
                                                
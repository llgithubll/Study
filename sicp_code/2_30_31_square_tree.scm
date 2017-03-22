(define (square x) (* x x))

; straight forward version
(define (square-tree tree)
    (cond ((null? tree) ())
            ((not (pair? tree)) (square tree))
            (else (cons (square-tree (car tree))
                        (square-tree (cdr tree))))))

; map version
(define (map proc items)
    (if (null? items)
        ()
        (cons (proc (car items))
                (map proc (cdr items)))))
(define (square-tree-map tree)
    (map (lambda (sub-tree)
            (if (pair? sub-tree)
                (square-tree-map sub-tree)
                (square sub-tree)))
        tree))

; tree map
(define (tree-map proc tree)
    (cond ((null? tree) ())
            ((not (pair? tree)) (proc tree))
            (else (cons (tree-map proc (car tree))
                        (tree-map proc (cdr tree))))))
(define (square-tree-map2 tree) (tree-map square tree))

(define x (list 1 (list 2 (list 3 4) 5)))
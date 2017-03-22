;;vector
(define (make-vect x y)
    (cons x y))

(define (xcor-vect v)
    (car v))

(define (ycor-vect v)
    (cdr v))

(define (add-vect v w)
    (cons (+ (xcor-vect v) (xcor-vect w))
            (+ (ycor-vect v) (ycor-vect w))))

(define (sub-vect v w)
    (cons (- (xcor-vect v) (xcor-vect w))
            (- (ycor-vect v) (ycor-vect w))))

(define (scale-vect v s)
    (cons (* s (xcor-vect)) (* s (ycor-vect))))

;;frame
(define (make-frame origin edge1 edge2)
    (list origin edge1 edge2))

(define (ori-frame f)
    (car f))

(define (e1-frame f)
    (cadr f))

(define (e2-frame f)
    (caddr f))

;;segment
(define (make-segment o-to-start o-to-end)
    (cons o-to-start o-to-end))

(define (start-segment segment)
    (car segment))

(define (end-segment segment)
    (cdr segment))


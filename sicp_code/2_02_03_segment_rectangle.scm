; segment
(define (make-segment start-point end-point)
    (cons start-point end-point))

(define (start-segment segment) (car segment))
(define (end-segment segment) (cdr segment))

(define (make-point x y)
    (cons x y))

(define (x-point point) (car point))
(define (y-point point) (cdr point))

(define (midpoint-segment segment)
    (make-point
        (/ (+ (x-point (start-segment segment))
                (x-point (end-segment segment)))
            2)
        (/ (+ (y-point (start-segment segment))
                (y-point (end-segment segment)))
            2)))

(define (print-point p)
    (newline)
    (display "(")
    (display (x-point p))
    (display ",")
    (display (y-point p))
    (display ")"))

(define s (make-point 1.0 1.0))
(define e (make-point 3.0 3.0))
(define seg (make-segment s e))
(print-point (midpoint-segment seg))

; rectangle
(define (make-rectangle left-up right-below)
    (cons left-up right-below))

(define (left-up-rect rectangle)
    (car rectangle))
(define (right-below-rect rectangle)
    (cdr rectangle))

(define (perimeter rectangle)
    (define (double x) (* 2 x))
    (+ (double (abs (- (x-point (left-up-rect rectangle))
                        (x-point (right-below-rect rectangle)))))
        (double (abs (- (y-point (left-up-rect rectangle))
                        (y-point (right-below-rect rectangle)))))))

(define (area rectangle)
    (abs (* (- (x-point (left-up-rect rectangle))
                (x-point (right-below-rect rectangle)))
            (- (y-point (left-up-rect rectangle))
                (y-point (right-below-rect rectangle))))))

(define rect (make-rectangle (make-point 0.0 2.0)
                                (make-point 4.0 0.0)))
(perimeter rect)
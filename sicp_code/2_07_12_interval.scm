(define (make-interval a b)
    (cons a b))

(define (lower-bound interval) (min (car interval) (cdr interval)))
(define (upper-bound interval) (max (car interval) (cdr interval)))

(define (add-interval x y)
    (make-interval (+ (lower-bound x) (lower-bound y))
                    (+ (upper-bound x) (upper-bound y))))

(define (sub-interval x y)
    (make-interval (- (lower-bound x) (upper-bound y))
                    (- (upper-bound x) (lower-bound y))))

(define (mul-interval x y)
    (let ((p1 (* (lower-bound x) (lower-bound y)))
            (p2 (* (lower-bound x) (upper-bound y)))
            (p3 (* (upper-bound x) (lower-bound y)))
            (p4 (* (upper-bound x) (upper-bound y))))
        (make-interval (min p1 p2 p3 p4)
                        (max p1 p2 p3 p4))))

(define (div-interval x y)
    (if (>= 0 (* (lower-bound y) (upper-bound y)))
        (error "Division error(interval spans 0)")
        (mul-interval x
                        (make-interval (/ 1.0 (upper-bound y))
                                        (/ 1.0 (lower-bound y))))))

(define (display-interval i)
    (newline)
    (display "[")
    (display (lower-bound i))
    (display ",")
    (display (upper-bound i))
    (display "]"))

(define (make-center-width c w)
    (make-interval (- c w) (+ c w)))

(define (center i)
    (/ (+ (lower-bound i) (upper-bound i)) 2))

(define (width i)
    (/ (- (upper-bound i) (lower-bound i)) 2))

(define (make-center-percent c p)
    (make-center-width c (* c p)))

(define (percent i)
    (/ (width i) (center i)))

                            
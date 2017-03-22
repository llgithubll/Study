;(define (cont-frac n d k)
;    (if (= k 0)
;        0
;        (/ (n k) (+ (d k) (cont-frac n d (- k 1))))))

(define (cont-frac n d k)
    (define (inc i) (+ i 1))
    (define (recur i)
        (if (> i k)
            0
            (/ (n i) (+ (d i) (recur (inc i))))))
    (recur 1))

;1_37
(cont-frac (lambda (i) 1.0) (lambda (i) 1.0) 10)

;1_38
(define (d i)
    (if (= 2 (remainder i 3))
        (* 2 (/ (+ i 1) 3))
        1.0))

(+ (cont-frac (lambda (i) 1.0) d 100) 2)
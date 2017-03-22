(define (pascal-triangle n)
    (define (cal-number col row)
        (cond ((= row 1) "\n1")
            ((= col 1) 1)
            ((= col row) 1)
            (else (+ (cal-number (- col 1) (- row 1))
                    (cal-number col (- row 1))))))
    (define (pascal-line now total)
        (define (display-line-interal now total)
            (display (cal-number now total))
            (cond ((< now total) (display-line-interal (+ now 1) total))))
        (display-line-interal 1 now)
        (display "\n")
        (cond ((< now total) (pascal-line (+ 1 now) total))))
    (pascal-line 1 n))

(pascal-triangle 5)
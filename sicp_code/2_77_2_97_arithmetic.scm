;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                      generic                              ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;using drop to get simplify answer
;;(define (add x y) (drop (apply-generic 'add x y)))      ;; scheme-number & rational & complex
;;(define (sub x y) (drop (apply-generic 'sub x y)))      ;; scheme-number & rational & complex
;;(define (mul x y) (drop (apply-generic 'mul x y)))      ;; scheme-number & rational & complex
;;(define (div x y) (drop (apply-generic 'div x y)))      ;; scheme-number & rational & complex

;;the comment indicate the implementation of deferent data type
;;note: rational: original rational, rf: rational fraction

(define (add x y) (apply-generic 'add x y))             ;; OK:scheme-number & rational & complex & polynomial & rf
(define (sub x y) (apply-generic 'sub x y))             ;; OK:scheme-number & rational & complex & polynomial & rf
(define (mul x y) (apply-generic 'mul x y))             ;; OK:scheme-number & rational & complex & polynomial & rf
(define (div x y) (apply-generic 'div x y))             ;; OK:scheme-number & rational & complex & polynomial & rf
(define (equ? x y) (apply-generic 'equ? x y))           ;; OK:scheme-number & rational & complex & polynomial & rf
(define (=zero? x) (apply-generic '=zero? x))           ;; OK:scheme-number & rational & complex & polynomial & rf
(define (raise x) (apply-generic 'raise x))             ;; OK:scheme-number & rational
(define (project x) (apply-generic 'project x))         ;; OK:              & rational & complex
(define (sine x) (apply-generic 'sine x))               ;; OK:scheme-number & rational
(define (cosine x) (apply-generic 'cosine x))           ;; OK:scheme-number & rational
(define (negate x) (apply-generic 'negate x))           ;; OK:scheme-number & rational & complex & polynomial & rf
(define (reduce x y) (apply-generic 'reduce x y))       ;; OK:scheme-number                      & polynomial
(define (greatest-common-divisor x y)                   ;; OK:scheme-number                      & polynomial
    (apply-generic 'greatest-common-divisor x y))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                      constructor                          ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (make-scheme-number n)
    ((get 'make 'scheme-number) n))
(define (make-rational n d)
    ((get 'make 'rational) n d))
(define (make-complex-from-real-imag x y)
    ((get 'make-from-real-imag 'complex) x y))
(define (make-complex-from-mag-ang r a)
    ((get 'make-from-mag-ang 'complex) r a))
(define (make-polynomial var terms)
    ((get 'make 'polynomial) var terms))
    
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                      utility                              ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; (define (attach-tag type-tag contents)
;;     (cons type-tag contents))

;; (define (type-tag datum)
;;     (if (pair? datum)
;;         (car datum)
;;         (error "Bad tagged datum -- TYPE-TAG" datum)))

;; (define (contents datum)
;;     (if (pair? datum)
;;         (cdr datum)
;;         (error "Bad tagged datum -- CONTENTS" datum)))
;;2_78
(define (attach-tag type-tag contents)
    (if (number? contents)
        contents
        (cons type-tag contents)))

(define (type-tag datum)
    (cond ((number? datum) 'scheme-number)
          ((pair? datum) (car datum))
          (else (error "Bad tagged datum -- TYPE-TAG" datum))))

(define (contents datum)
    (cond ((number? datum) datum)
          ((pair? datum) (cdr datum))
          (else (error "Bad tagged datum -- TYPE-TAG" datum))))

(define (square x) (* x x))

;;;;original version
;;(define (apply-generic op . args)
;;    (let ((type-tags (map type-tag args)))
;;        (let ((proc (get op type-tags)))
;;            (if proc
;;                (apply proc (map contents args))
;;                (error "No method for these types -- APPLY-GENERIC"
;;                        (list op type-tags))))))

;;;;apply-generic coercion version
;; (define (apply-generic op . args) 
;;    (define (no-method type-tags) 
;;      (error "No method for these types" 
;;        (list op type-tags))) 
;;
;;    (let ((type-tags (map type-tag args))) 
;;      (let ((proc (get op type-tags))) 
;;        (if proc 
;;            (apply proc (map contents args)) 
;;            (if (= (length args) 2) 
;;                (let ((type1 (car type-tags)) 
;;                      (type2 (cadr type-tags)) 
;;                      (a1 (car args)) 
;;                      (a2 (cadr args))) 
;;                  (if (equal? type1 type2) 
;;                    (no-method type-tags) 
;;                    (let ((t1->t2 (get-coercion type1 type2)) 
;;                          (t2->t1 (get-coercion type2 type1)) 
;;                          (a1 (car args)) 
;;                          (a2 (cadr args))) 
;;                      (cond (t1->t2 
;;                             (apply-generic op (t1->t2 a1) a2)) 
;;                            (t2->t1 
;;                             (apply-generic op a1 (t2->t1 a2))) 
;;                            (else (no-method type-tags)))))) 
;;                (no-method type-tags))))))



;;raise
(define (level type)
    (cond ((eq? type 'scheme-number) 0)
          ((eq? type 'rational) 1)
          ((eq? type 'complex) 2)
          (else (error "Invalid type -- LEVEL" type))))

;;;;raise version
(define (apply-generic op . args)
    (let ((type-tags (map type-tag args)))
        (define (no-method)
            (error "No method for these types" (list op type-tags)))
        (let ((proc (get op type-tags)))
            (if proc
                (apply proc (map contents args))       ;raise version
                (if (not (null? (cdr args)))
                    (let ((raised-args (raise-to-common args)))
                        (if raised-args
                            (let ((proc (get op (map type-tag raised-args))))
                                (if proc
                                    (apply proc (map contents raised-args))
                                    (no-method)))
                            (no-method)))
                    (no-method))))))

(define (raise-to-common args)
    (let ((raised-args
            (map (lambda (x) (raise-to-type (highest-type args) x))
                 args)))
        (if (all-true? raised-args)
            raised-args
            #f)))

(define (all-true? lst)
    (cond ((null? lst) #t)
          ((car lst) (all-true? (cdr lst)))
          (else #f)))

(define (raise-to-type type item)
    (let ((item-type (type-tag item)))
        (if (eq? item-type type)
            item
            (let ((raise-fn (get 'raise item-type)))
                (if raise-fn
                    (raise-to-type type (raise-fn item))
                    #f)))))

(define (highest-type args)
    (if (null? (cdr args))
        (type-tag (car args))
        (let ((t1 (type-tag (car args)))
              (t2 (highest-type (cdr args))))
            (let ((l1 (level t1))
                  (l2 (level t2)))
                (if (> l1 l2)
                    t1
                    t2)))))                        

;;drop
(define (drop x)
    (if (eq? (type-tag x) 'scheme-number)
        x
        (if (equ? (raise (project x)) x)
            (drop (project x))
            x)))


;;put & get
(define global-array '())

(define (make-entry k v) (list k v))
(define (key entry) (car entry))
(define (value entry) (cadr entry))

(define (put op type item)
  (define (put-helper k array)
    (cond ((null? array) (list(make-entry k item)))
          ((equal? (key (car array)) k) array)
          (else (cons (car array) (put-helper k (cdr array))))))
  (set! global-array (put-helper (list op type) global-array)))

(define (get op type)
  (define (get-helper k array)
    (cond ((null? array) #f)
          ((equal? (key (car array)) k) (value (car array)))
          (else (get-helper k (cdr array)))))
  (get-helper (list op type) global-array))

;;coercion
(define *coercion-table* (make-equal-hash-table)) 
  
 (define (put-coercion type1 type2 proc) 
   (hash-table/put! *coercion-table* (list type1 type2) proc)) 
  
 (define (get-coercion type1 type2) 
   (hash-table/get *coercion-table* (list type1 type2) '())) 
  
 (define (install-coercion-package) 
 (define (scheme-number->complex n) 
   (make-complex-from-real-imag (contents n) 0)) 
 (define (scheme-number->rational n) 
   (make-rational (contents n) 1)) 
 (put-coercion 'scheme-number 'rational scheme-number->rational) 
 (put-coercion 'scheme-number 'complex scheme-number->complex) 
 'done) 
  
 (install-coercion-package)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                      scheme-number                        ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (install-scheme-number-package)
    (define (tag x) (attach-tag 'scheme-number x))
    (put 'add '(scheme-number scheme-number)
        (lambda (x y) (tag (+ x y))))
    (put 'sub '(scheme-number scheme-number)
        (lambda (x y) (tag (- x y))))
    (put 'mul '(scheme-number scheme-number)
        (lambda (x y) (tag (* x y))))
    (put 'div '(scheme-number scheme-number)
        (lambda (x y) (tag (/ x y))))
    (put 'equ? '(scheme-number scheme-number) =)
    (put '=zero? '(scheme-number)
        (lambda (x) (tag (= x 0))))
    (put 'raise '(scheme-number)    ;;scheme-number(integer) -> rational (-> complex)
        (lambda (x) (make-rational x 1)))
    (put 'sine '(scheme-number)
        (lambda (x) (tag (sin x))))
    (put 'cosine '(scheme-number)
        (lambda (x) (tag (cos x))))
    (put 'negate '(scheme-number)
        (lambda (x) (tag (- x))))
    (put 'reduce '(scheme-number scheme-number)
        (lambda (x y) (let ((g (gcd x y))) (cons (/ x g) (/ y g)))))
    (put 'greatest-common-divisor '(scheme-number scheme-number)
        (lambda (a b) (tag (gcd a b))))
    (put 'make 'scheme-number
        (lambda (x) (tag x)))
    'done)
(install-scheme-number-package) ;;execute install function

;;original rational(only for scheme-number)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;                      rational                             ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;(define (install-rational-package)
;;    ;;internal procedures
;;    (define (numer x) (car x))
;;    (define (denom x) (cdr x))
;;    (define (make-rat n d)
;;        (let ((g (gcd n d)))
;;            (cons (/ n g) (/ d g))))
;;    
;;    (define (add-rat x y)
;;        (make-rat (+ (* (numer x) (denom y))
;;                     (* (numer y) (denom x)))
;;                  (* (denom x) (denom y))))
;;    (define (sub-rat x y)
;;        (make-rat (- (* (numer x) (denom y))
;;                     (* (numer y) (denom x)))
;;                  (* (denom x) (denom y))))
;;    (define (mul-rat x y)
;;        (make-rat (* (numer x) (numer y))
;;                  (* (denom x) (denom y))))
;;    (define (div-rat x y)
;;        (make-rat (* (numer x) (denom y))
;;                  (* (denom x) (numer y))))
;;
;;    (define (equ? x y)
;;        (= (* (numer x) (denom y)) (* (numer y) (denom x))))
;;
;;    ;;interface to rest of the system
;;    (define (tag x) (attach-tag 'rational x))
;;    (put 'add '(rational rational)
;;        (lambda (x y) (tag (add-rat x y))))
;;    (put 'sub '(rational rational)
;;        (lambda (x y) (tag (sub-rat x y))))
;;    (put 'mul '(rational rational)
;;        (lambda (x y) (tag (mul-rat x y))))
;;    (put 'div '(rational rational)
;;        (lambda (x y) (tag (div-rat x y))))
;;    (put 'equ? '(rational rational) equ?)
;;    (put '=zero? '(rational)
;;        (lambda (x) (tag (= (numer x) 0))))
;;    (put 'raise '(rational)   ;;(scheme-number ->) rational -> complex
;;        (lambda (x) (make-complex-from-real-imag 
;;                            (/ (numer x) (denom x))
;;                            0)))
;;    (put 'project '(rational)
;;        (lambda (x) (make-scheme-number (round (/ (numer x) (denom x))))))
;;    (put 'sine '(rational)
;;        (lambda (x) (tag (sin (/ (numer x) (denom x))))))
;;    (put 'cosine '(rational)
;;        (lambda (x) (tag (cos (/ (numer x) (denom x))))))
;;    (put 'negate '(rational)
;;        (lambda (x) (make-rational (- (numer x)) (denom x))))
;;    (put 'make 'rational
;;        (lambda (n d) (tag (make-rat n d))))
;;    'done)
;;(install-rational-package) ;;execute install function


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                  rational                                 ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (install-rational-package)
    ;;internal procedures
    (define (numer x) (car x))
    (define (denom x) (cdr x))
    (define (make-rat p1 p2)
        (reduce p1 p2))
    
    (define (add-rat p1 p2)
        (make-rat (add (mul (numer p1) (denom p2))
                       (mul (numer p2) (denom p1)))
                  (mul (denom p1) (denom p2))))
    (define (sub-rat p1 p2)
        (make-rat (sub (mul (numer p1) (denom p2))
                       (mul (numer p2) (denom p1)))
                  (mul (denom p1) (denom p2))))
    (define (mul-rat p1 p2)
        (make-rat (mul (numer p1) (numer p2))
                  (mul (denom p1) (denom p2))))
    (define (div-rat p1 p2)
        (make-rat (mul (numer p1) (denom p2))
                  (mul (denom p1) (numer p2))))

    (define (equ-rational? x y)
        (equ? (mul (numer x) (denom y))
              (mul (numer y) (denom x))))
    ;;interface to rest of the system
    (define (tag x) (attach-tag 'rational x))
    (put 'add '(rational rational)
        (lambda (x y) (tag (add-rat x y))))
    (put 'sub '(rational rational)
        (lambda (x y) (tag (sub-rat x y))))
    (put 'mul '(rational rational)
        (lambda (x y) (tag (mul-rat x y))))
    (put 'div '(rational rational)
        (lambda (x y) (tag (div-rat x y))))
    (put 'equ? '(rational rational)
        (lambda (x y) (equ-rational? x y)))
    (put '=zero? '(rational)
        (lambda (x) (tag (=zero? (numer x)))))
    (put 'negate '(rational)
        (lambda (x) (make-rational (negate (numer x)) (denom x))))
    (put 'make 'rational
        (lambda (n d) (tag (make-rat n d))))
    'done)
(install-rational-package)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                      complex                              ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (install-rectangular-package)
    ;;internal procedures
    (define (real-part z) (car z))
    (define (imag-part z) (cdr z))
    (define (make-from-real-imag x y) (cons x y))
    (define (magnitude z)
        (sqrt (+ (square (real-part z))
                 (square (imag-part z)))))
    (define (angle z)
        (atan (imag-part z) (real-part z)))
    (define (make-from-mag-ang r a)
        (cons (* r (cos a)) (* r (sin a))))
        
    ;;interface to the rest of the system
    (define (tag x) (attach-tag 'rectangular x))
    (put 'real-part '(rectangular) real-part)
    (put 'imag-part '(rectangular) imag-part)
    (put 'magnitude '(rectangular) magnitude)
    (put 'angle '(rectangular) angle)
    (put 'make-from-real-imag 'rectangular
        (lambda (x y) (tag (make-from-real-imag x y))))
    (put 'make-from-mag-ang 'rectangular
        (lambda (r a) (tag (make-from-mag-ang r a))))
    'done)
(install-rectangular-package)   ;;execute install function

(define (install-polar-package)
    ;;internal procedures
    (define (magnitude z) (car z))
    (define (angle z) (cdr z))
    (define (make-from-mag-ang r a) (cons r a))
    (define (make-from-real-imag x y)
        (cons (sqrt (+ (square x) (square y)))
              (atan y x)))
    (define (real-part z)
        (* (magnitude z) (cos (angle z))))
    (define (imag-part z)
        (* (magnitude z) (sin (angle z))))
    
    ;;interface to the rest of the system
    (define (tag x) (attach-tag 'polar x))
    (put 'real-part '(polar) real-part)
    (put 'imag-part '(polar) imag-part)
    (put 'magnitude '(polar) magnitude)
    (put 'angle '(polar) angle)
    (put 'make-from-real-imag 'polar
        (lambda (x y) (tag (make-from-real-imag x y))))
    (put 'make-from-mag-ang 'polar
        (lambda (r a) (tag (make-from-mag-ang r a))))
    'done)
(install-polar-package) ;;execute install function

(define (real-part z) (apply-generic 'real-part z))
(define (imag-part z) (apply-generic 'imag-part z))
(define (magnitude z) (apply-generic 'magnitude z))
(define (angle z) (apply-generic 'angle z))

(define (install-complex-package)
    ;;imported procedures from rectangular and polar packages
    (define (make-from-real-imag x y)
        ((get 'make-from-real-imag 'rectangular) x y))
    (define (make-from-mag-ang r a)
        ((get 'make-from-mag-ang 'polar) r a))
    
    ;;internal procedures
    (define (add-complex z1 z2)
        (make-from-real-imag (+ (real-part z1) (real-part z2))
                             (+ (imag-part z1) (imag-part z2))))
    (define (sub-complex z1 z2)
        (make-from-real-imag (- (real-part z1) (real-part z2))
                             (- (imag-part z1) (imag-part z2))))
    (define (mul-complex z1 z2)
        (make-from-mag-ang (* (magnitude z1) (magnitude z2))
                           (+ (angle z1) (angle z2))))
    (define (div-complex z1 z2)
        (make-from-mag-ang (/ (magnitude z1) (magnitude z2))
                           (- (angle z1) (angle z2))))
    (define (equ? x y)
        (and (= (real-part x) (real-part y))
             (= (imag-part x) (imag-part y))))

    ;;interface to rest of system
    (define (tag z) (attach-tag 'complex z))
    (put 'add '(complex complex)
        (lambda (z1 z2) (tag (add-complex z1 z2))))
    (put 'sub '(complex complex)
        (lambda (z1 z2) (tag (sub-complex z1 z2))))
    (put 'mul '(complex complex)
        (lambda (z1 z2) (tag (mul-complex z1 z2))))
    (put 'div '(complex complex)
        (lambda (z1 z2) (tag (div-complex z1 z2))))
    (put 'equ? '(complex complex) equ?)
    (put '=zero? '(complex)
        (lambda (x) (tag (= (real-part x) (imag-part x) 0))))
    (put 'project '(complex)
        (lambda (x)
            (let ((rat (rationalize (inexact->exact (real-part x)) 1/100)))
                (make-rational (numerator rat) (denominator rat)))))
    (put 'negate '(complex)
        (lambda (x) (make-from-real-imag (- (real-part x)) (- (imag-part x)))))
    (put 'make-from-real-imag 'complex
        (lambda (x y) (tag (make-from-real-imag x y))))
    (put 'make-from-mag-ang 'complex
        (lambda (r a) (tag (make-from-mag-ang r a))))
    'done)
(install-complex-package)   ;;execute install function

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;                      polynomial                           ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (install-polynomial-package)
    ;;internal procedures
    ;;representation of poly
    (define (make-poly variable term-list)
        (cons variable term-list))
    (define (variable p) (car p))
    (define (term-list p) (cdr p))
    (define (variable? x) (symbol? x))
    (define (same-variable? v1 v2)
        (and (variable? v1) (variable? v2) (eq? v1 v2)))
    (define (=zero? x)
        (cond ((number? x) (= x 0))
              ((pair? x) (empty-termlist? (term-list x)))
              (else (error "Unknown type -- =ZERO?(polynomial)" x))))
    
    ;;representation of terms and term lists

    ;;assume term-list is ordered, and term has highest order in term-list
    (define (adjoin-term term term-list)    
        (if (=zero? (coeff term))
            term-list
            (cons term term-list)))
    
    (define (the-empty-termlist) '())
    (define (first-term term-list) (car term-list))
    (define (rest-terms term-list) (cdr term-list))
    (define (empty-termlist? term-list) (null? term-list))
    
    (define (make-term order coeff) (list order coeff))
    (define (order term) (car term))
    (define (coeff term) (cadr term))
    
    (define (add-terms L1 L2)
        (cond ((empty-termlist? L1) L2)
              ((empty-termlist? L2) L1)
              (else (let ((t1 (first-term L1)) (t2 (first-term L2)))
                        (cond ((> (order t1) (order t2))
                                    (adjoin-term t1 (add-terms (rest-terms L1) L2)))
                              ((< (order t1) (order t2))
                                    (adjoin-term t2 (add-terms L1 (rest-terms L2))))
                              (else (adjoin-term
                                        (make-term (order t1)
                                                   (add (coeff t1) (coeff t2)))
                                        (add-terms (rest-terms L1) (rest-terms L2)))))))))

    (define (add-poly p1 p2)
        (if (same-variable? (variable p1) (variable p2))
            (make-poly (variable p1)
                       (add-terms (term-list p1)
                                  (term-list p2)))
            (error "Polys not in same var -- ADD-POLY" (list p1 p2))))

    (define (mul-terms L1 L2)
        (if (empty-termlist? L1)
            (the-empty-termlist)
            (add-terms (mul-term-by-all-terms (first-term L1) L2)
                       (mul-terms (rest-terms L1) L2))))
    (define (mul-term-by-all-terms t1 L)
        (if (empty-termlist? L)
            (the-empty-termlist)
            (let ((t2 (first-term L)))
                (adjoin-term
                    (make-term (+ (order t1) (order t2))
                               (mul (coeff t1) (coeff t2)))
                    (mul-term-by-all-terms t1 (rest-terms L))))))
    (define (mul-poly p1 p2)
        (if (same-variable? (variable p1) (variable p2))
            (make-poly (variable p1)
                       (mul-terms (term-list p1)
                                  (term-list p2)))
            (error "Polys not in same var -- MUL-POLY" (list p1 p2))))
    
    (define (negate-terms termlist) 
        (if (empty-termlist? termlist) 
            (the-empty-termlist) 
            (let ((t (first-term termlist))) 
                (adjoin-term (make-term (order t) (negate (coeff t))) 
                             (negate-terms (rest-terms termlist))))))

    (define (div-terms L1 L2)
        (if (empty-termlist? L1)
            (list (the-empty-termlist) (the-empty-termlist))
            (let ((t1 (first-term L1))
                  (t2 (first-term L2)))
                (if (> (order t2) (order t1))
                    (list (the-empty-termlist) L1)
                    (let ((new-c (div (coeff t1) (coeff t2)))
                          (new-o (- (order t1) (order t2))))
                        (let ((rest-of-result
                                (div-terms 
                                    (add-terms L1
                                               (negate-terms (mul-terms (list (make-term new-o new-c))
                                                                        L2)))
                                    L2)))
                            (list (adjoin-term (make-term new-o new-c) (car rest-of-result))
                                  (cadr rest-of-result))))))))
                    
    (define (div-poly p1 p2)
        (if (same-variable? (variable p1) (variable p2))
            (let ((result (div-terms (term-list p1)
                                     (term-list p2))))
                (list (make-poly (variable p1) (car result))
                      (make-poly (variable p2) (cadr result))))
            (error "Variable is not the same -- DIV-POLY"
                (list (variable p1) (variable p2)))))

    (define (remainder-terms p1 p2)
        (cadr (div-terms p1 p2)))
    (define (pseudoremainder-terms a b) 
        (let* ((o1 (order (first-term a))) 
               (o2 (order (first-term b))) 
               (c (coeff (first-term b))) 
               (divident (mul-term-by-all-terms (make-term 0 (expt c (+ 1 (- o1 o2)))) 
                                                a))) 
              (cadr (div-terms divident b))))
    
    (define (gcd-terms a b)
        (if (empty-termlist? b)
            (let* ((coeff-list (map cadr a))
                   (gcd-coeff (apply gcd coeff-list)))
                  (car (div-terms a (list (make-term 0 gcd-coeff))))) ;; (list (make-term 0 gcd-coeff)) : term -> terms
            (gcd-terms b (pseudoremainder-terms a b))))
    (define (gcd-poly p1 p2)
        (if (same-variable? (variable p1) (variable p2))
            (make-poly (variable p1)
                       (gcd-terms (term-list p1)
                                  (term-list p2)))
            (error "Not the same variable --GCD-POLY" (list p1 p2))))

    (define (reduce-terms n d)
        (let ((gcdterms (gcd-terms n d)))
            (list (car (div-terms n gcdterms))
                  (car (div-terms d gcdterms)))))
    (define (reduce-poly p1 p2)
        (if (same-variable? (variable p1) (variable p2))
            (let ((result (reduce-terms (term-list p1) (term-list p2))))
                (list (make-poly (variable p1) (car result))
                      (make-poly (variable p2) (cadr result))))
            (error "Not the same variable -- REDUCE-POLY" (list p1 p2))))

    (define (equ-terms? L1 L2)
        (cond ((empty-termlist? L1) (empty-termlist? L2))
              ((empty-termlist? L2) (empty-termlist? L1))
              (else (let ((t1 (first-term L1)) (t2 (first-term L2)))
                          (and (equ? (order t1) (order t2))
                               (equ? (coeff t1) (coeff t2))
                               (equ-terms? (rest-terms L1) (rest-terms L2)))))))
    (define (equ-poly? p1 p2)
        (if (same-variable? (variable p1) (variable p2))
            (equ-terms? (term-list p1) (term-list p2))
            #f))
    ;;interface to rest of the system
    (define (tag p) (attach-tag 'polynomial p))
    (put 'add '(polynomial polynomial)
        (lambda (p1 p2) (tag (add-poly p1 p2))))
    (put 'sub '(polynomial polynomial)
        (lambda (x y) (tag (add-poly x
                                     (make-poly (variable y) (negate-terms (term-list y)))))))
    (put 'mul '(polynomial polynomial)
        (lambda (p1 p2) (tag (mul-poly p1 p2))))
    (put 'div '(polynomial polynomial)
        (lambda (x y) (tag (div-poly x y))))
    (put 'equ? '(polynomial polynomial)
        (lambda (p1 p2) (equ-poly? p1 p2)))
    (put '=zero? '(polynomial)
        (lambda (x) (tag (=zero? x))))
    (put 'negate '(polynomial)
        (lambda (x) (tag (make-poly (variable x)
                               (negate-terms (term-list x))))))
    (put 'reduce '(polynomial polynomial)
        (lambda (p1 p2) (let ((reducedpolys (reduce-poly p1 p2)))
                            (cons (tag (car reducedpolys)) (tag (cadr reducedpolys))))))
    (put 'greatest-common-divisor '(polynomial polynomial)
        (lambda (p1 p2) (tag (gcd-poly p1 p2))))
    (put 'make 'polynomial
        (lambda (var terms) (tag (make-poly var terms))))  
    'done)
(install-polynomial-package)

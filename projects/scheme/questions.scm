; Some utility functions that you may find useful.
(define (apply-to-all proc items)
  (if (null? items)
      '()
      (cons (proc (car items))
            (apply-to-all proc (cdr items)))))

(define (keep-if predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (keep-if predicate (cdr sequence))))
        (else (keep-if predicate (cdr sequence)))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdr (car x))))

; Problem 18
;; Turns a list of pairs into a pair of lists
(define (zip pairs)
  (define (helper-first pairs)                                                ; Helper function that returns... 
    (cond ((null? pairs) nil)                                                 ; ...a list of the first items of each element of pairs
          (else (cons (caar pairs) (helper-first (cdr pairs))))               
      ))
  (define (helper-second pairs)                                               ; Helper function that returns
    (cond ((null? pairs) nil)                                                 ; ...a list of the second items of each element of pairs
          (else (cons (cadr (car pairs)) (helper-second (cdr pairs))))        
      ))
  (cons (helper-first pairs) (list (helper-second pairs))))                    ; Return a pair with a list of the first and second elements respectively

(zip '())
; expect (() ())
(zip '((1 2)))
; expect ((1) (2))
(zip '((1 2) (3 4) (5 6)))
; expect ((1 3 5) (2 4 6))

; Problem 19

;; A list of all ways to partition TOTAL, where  each partition must
;; be at most MAX-VALUE and there are at most MAX-PIECES partitions.

(define (helper value lst)                                                ; Creates a helper that adds a value to the beginning to the beginning of a list
  (cond ((null? lst) nil)
        (else (cons (cons value (car lst)) (helper value (cdr lst))))
  ))

(define (list-partitions total max-pieces max-value)
  (cond ((> max-value total) (list-partitions total max-pieces total))                                    ; Checks to make sure that max-value is not greater than total
        ((= total 0) (list nil))                                                                          ; Base case to end recursion
        ((> total (* max-pieces max-value)) nil)                                                          ; Checks that it is feasible to have a partition for a number with the pieces and max value
        ((= 1 max-pieces) (cons (cons total nil) nil))                                                    ; If the pieces is 1, return the total value
        (else (append (helper max-value (list-partitions (- total max-value) (- max-pieces 1) max-value)) ; Add the elements to the recursion of lower max value and pieces and append that to the recursion of only lowering the maxvalue
              (list-partitions total max-pieces (- max-value 1))))
  ))

(list-partitions 5 2 4)
; expects a permutation of ((4 1) (3 2))
(list-partitions 7 3 5)
; expects a permutation of ((5 2) (5 1 1) (4 3) (4 2 1) (3 3 1) (3 2 2))


; Problem 20
;; Returns a function that takes in an expression and checks if it is the special
;; form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (analyze expr)
  (cond ((atom? expr) expr)                                                                   ; Return the value if it is a simple value
        ((quoted? expr) expr)                                                                 ; Return the value as it is, because it is quoted
        ((or (lambda? expr)                                                                   
             (define? expr))  
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           (cons form (cons params (apply-to-all analyze body)))                              ; Turns a let function into a define function
         )
        )
        ((let? expr)
         (let  ((values (cadr expr))
               (body   (cddr expr)))
                (begin (define parame (car (zip values)))                                     ; Seperate the original let function values with the zip function to get parameters
                       (define val (apply-to-all analyze (car (cdr (zip values)))))           ; Seperate the original let function values with the zip function to get the values to the parameters
                       (cons (cons 'lambda (cons parame (apply-to-all analyze body))) val)    ; Translates the let function into a lambda function with values to be evaluated
                )
              )
        )
        (else (apply-to-all analyze expr))))                                                   ; Evaluate the expression if it consists of more than one expression with the apply to all function
        
(analyze 1)
; expect 1
(analyze 'a)
; expect a
(analyze '(+ 1 2))
; expect (+ 1 2)

;; Quoted expressions remain the same
(analyze '(quote (let ((a 1) (b 2)) (+ a b))))
; expect (quote (let ((a 1) (b 2)) (+ a b)))

;; Lambda parameters not affected, but body affected
(analyze '(lambda (let a b) (+ let a b)))
; expect (lambda (let a b) (+ let a b))
(analyze '(lambda (x) a (let ((a x)) a)))
; expect (lambda (x) a ((lambda (a) a) x))

(analyze '(let ((a 1)
                (b 2))
            (+ a b)))
; expect ((lambda (a b) (+ a b)) 1 2)
(analyze '(let ((a (let ((a 2)) a))
                (b 2))
            (+ a b)))
; expect ((lambda (a b) (+ a b)) ((lambda (a) a) 2) 2)
(analyze '(let ((a 1))
            (let ((b a))
              b)))
; expect ((lambda (a) ((lambda (b) b) a)) 1)


;; Problem 21 (optional)
;; Draw the hax image using turtle graphics.
(define (hax d k)
  'YOUR-CODE-HERE
  nil)





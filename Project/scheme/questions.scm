(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; 第 15 题
;; 返回由双元素列表组成的列表
(define (enumerate s)
  ; BEGIN PROBLEM 15
  'replace-this-line
  )
  ; END PROBLEM 15

;; 第 16 题

;; 按照 ORDERED? 合并两个列表 S1 和 S2，并返回
;; 合并后的列表。
(define (merge ordered? s1 s2)
  ; BEGIN PROBLEM 16
  'replace-this-line
  )
  ; END PROBLEM 16

;; 选做题 2

;; 返回一个函数，用于检查表达式是否为特殊形式 FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; 将 EXPR 中所有 let 特殊形式转换为使用 lambda 的等价形式
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN OPTIONAL PROBLEM 2
         'replace-this-line
         ; END OPTIONAL PROBLEM 2
         )
        ((quoted? expr)
         ; BEGIN OPTIONAL PROBLEM 2
         'replace-this-line
         ; END OPTIONAL PROBLEM 2
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
           'replace-this-line
           ; END OPTIONAL PROBLEM 2
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
           'replace-this-line
           ; END OPTIONAL PROBLEM 2
           ))
        (else
         ; BEGIN OPTIONAL PROBLEM 2
         'replace-this-line
         ; END OPTIONAL PROBLEM 2
         )))

; 实现 let-to-lambda 时可能有用的一些辅助函数

(define (zip pairs)
  'replace-this-line)

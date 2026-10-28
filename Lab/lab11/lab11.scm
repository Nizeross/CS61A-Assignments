(define (if-program condition if-true if-false)
  'YOUR-CODE-HERE)

(define (square n) (* n n))

(define (pow-expr base exp) 'YOUR-CODE-HERE)

(define-macro (repeat n expr)
  `(repeated-call ,n ___))

; 调用无参数过程 f 共 n 次，返回最后一次的结果。
(define (repeated-call n f)
  (if (= n 1)
      ___
      (begin ___ ___)))

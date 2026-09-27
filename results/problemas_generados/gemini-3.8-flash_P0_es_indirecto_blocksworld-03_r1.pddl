(define (problem bloques-torre)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (handempty)
    (clear a)
    (on a d)
    (on d b)
    (on b f)
    (on f e)
    (on e c)
    (ontable c)
  )
  (:goal
    (and
      (on e f)
      (on f a)
      (on a b)
      (on b c)
      (on c d)
    )
  )
)

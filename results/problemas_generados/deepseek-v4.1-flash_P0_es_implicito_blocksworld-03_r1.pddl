(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
  )
  (:init
    (ontable c)
    (on e c)
    (on f e)
    (on b f)
    (on d b)
    (on a d)
    (clear a)
    (handempty)
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
